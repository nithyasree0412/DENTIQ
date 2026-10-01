import json

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


class RAGService:

    def __init__(
        self,
        embedding_service,
        milvus_service,
        llm_service
    ):

        self.embedding_service = embedding_service
        self.milvus_service = milvus_service
        self.llm_service = llm_service

    def answer_doubt(
        self,
        user_query,
        subject_id,
        score_threshold=0.72
    ):

        query_embedding = (
            self.embedding_service.embed_query(
                user_query
            )
        )

        search_results = self.milvus_service.search(
            query_embedding,
            subject_id,
            limit=5
        )

        relevant_results = [
            result
            for result in search_results[0]
            if result["distance"] >= score_threshold
        ]

        if not relevant_results:

            return (
                "I couldn't find the answer "
                "in the provided study material."
            )

        context_parts = []

        for result in relevant_results:

            text = result["entity"]["text"]
            page = result["entity"]["page"]

            context_parts.append(
                f"[Page {page}]\n{text}"
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are a helpful study assistant.

Answer the user's question using ONLY the provided study material.

If the answer cannot be found in the study material, say:

"I couldn't find the answer in the provided study material."

Do not use outside knowledge or assumptions.

User question:

{user_query}

Study material:

{context}

Give a clear and concise answer suitable for an engineering student.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful study assistant. "
                    "Answer only from the provided study material."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        final_answer = self.llm_service.generate(
            messages
        )

        return final_answer

    def mmr_select(
        self,
        candidate_embeddings,
        num_select=12,
        diversity_weight=0.7
    ):

        similarity_matrix = cosine_similarity(
            candidate_embeddings
        )

        selected_indices = []

        remaining_indices = list(
            range(
                len(candidate_embeddings)
            )
        )

        num_select = min(
            num_select,
            len(candidate_embeddings)
        )

        while (
            remaining_indices
            and len(selected_indices) < num_select
        ):

            if not selected_indices:

                selected_index = np.random.choice(
                    remaining_indices
                )

            else:

                scores = []

                for candidate_index in remaining_indices:

                    selected_similarities = (
                        similarity_matrix[
                            candidate_index
                        ][
                            selected_indices
                        ]
                    )

                    redundancy = max(
                        selected_similarities
                    )

                    diversity_score = (
                        1 - redundancy
                    )

                    score = (
                        diversity_weight
                        * diversity_score
                    )

                    scores.append(score)

                best_position = np.argmax(
                    scores
                )

                selected_index = remaining_indices[
                    best_position
                ]

            selected_indices.append(
                selected_index
            )

            remaining_indices.remove(
                selected_index
            )

        return selected_indices

    def generate_test(
        self,
        subject_id,
        num_questions
    ):

        candidates = (
            self.milvus_service.get_random_candidates(
                subject_id=subject_id,
                num_candidates=40
            )
        )

        if not candidates:

            return {
                "message": (
                    "No study material found "
                    "for this subject."
                )
            }

        candidate_embeddings = np.array([
            candidate["vector"]
            for candidate in candidates
        ])

        selected_indices = self.mmr_select(
            candidate_embeddings=candidate_embeddings,
            num_select=12,
            diversity_weight=0.7
        )

        selected_chunks = [
            candidates[index]["text"]
            for index in selected_indices
        ]

        context = "\n\n".join(
            selected_chunks
        )

        system_prompt = """
You are an MCQ question generator.

Your task is to generate high-quality multiple-choice
questions strictly from the study material provided by the user.

STRICT RULES:

1. Use ONLY the provided study material.
2. Do not use outside knowledge.
3. Generate exactly the requested number of questions.
4. Every question must be complete and meaningful.
5. Every question must have exactly 4 options.
6. The options must be A, B, C, and D.
7. All four options must be different.
8. Only ONE option can be correct.
9. The correct answer must be supported by the study material.
10. Do not create duplicate questions.
11. Do not create duplicate or nearly identical options.
12. Avoid questions where the answer is unclear from the study material.
13. Cover different concepts when possible.
14. Return ONLY valid JSON.
15. Do not add markdown.
16. Do not add explanations outside the JSON.
"""

        user_prompt = f"""
Generate exactly {num_questions} multiple-choice questions
from the following study material.

Study material:

{context}

Return the response using EXACTLY this JSON structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "answer": "A"
        }}
    ]
}}

The "questions" array must contain exactly {num_questions} questions.

The "answer" field must contain only:
"A", "B", "C", or "D".
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        test_answer = self.llm_service.generate(
            messages,
            max_new_tokens=2000,
            temperature=0.5,
            top_p=0.9
        )

        test_answer = test_answer.strip()

        if test_answer.startswith("```json"):
            test_answer = test_answer[7:]

        if test_answer.endswith("```"):
            test_answer = test_answer[:-3]

        test_answer = test_answer.strip()

        try:

            test_data = json.loads(
                test_answer
            )

        except json.JSONDecodeError:

            return {
                "error": "Invalid JSON generated by the model.",
                "raw_response": test_answer
            }

        if isinstance(test_data, list):

            test_data = {
                "questions": test_data
            }

        questions = test_data.get(
            "questions",
            []
        )

        if len(questions) != num_questions:

            return {
                "error": (
                    f"Expected {num_questions} questions "
                    f"but model generated {len(questions)}."
                ),
                "data": test_data
            }

        questions = []

        for index, question in enumerate(
            test_data["questions"]
        ):

            questions.append({
                "questionId": index + 1,
                "question": question["question"],
                "options": question["options"],
                "answer": question["answer"]
            })

        return {
            "questions": questions
        }