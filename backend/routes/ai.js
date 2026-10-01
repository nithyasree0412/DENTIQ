import Router from 'express';
import { authMiddleware } from '../middleware/auth.js';
import { Test, TestAttempt } from '../db.js';

const router = Router();

router.post('/test', authMiddleware, async (req, res) => {

    const response = await fetch(
        'http://localhost:8000/api/v1/rag/test',
        {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(req.body)
        }
    );

    const data = await response.json();

    const questions = data.result.questions;

    const test = await Test.create({
        subjectId: req.body.subjectId,
        questions: questions
    });

    const questionsForFrontend = questions.map(
        ({ question, options }) => ({
            question,
            options
        })
    );

    res.json({
        testId: test._id,
        questions: questionsForFrontend
    });
});

router.post('/test/submit', authMiddleware, async (req, res) => {

    const { testId, answers } = req.body;

    const test = await Test.findById(testId);

    if (!test) {
        return res.status(404).json({
            message: "Test not found"
        });
    }

    let score = 0;

    test.questions.forEach((question, index) => {

        const userAnswer = answers[index + 1];

        if (userAnswer === question.answer) {
            score++;
        }
    });

    const testAttempt = await TestAttempt.create({
        userId: req.userId,
        testId: test._id,
        subjectId: test.subjectId,
        answers: answers,
        score: score,
        totalQuestions: test.questions.length
    });

    res.json({
        attemptId: testAttempt._id,
        score: score,
        totalQuestions: test.questions.length
    });
});

router.post('/doubt', authMiddleware, async (req, res) => {

    const response = await fetch(
        'http://localhost:8000/api/v1/rag/doubt',
        {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(req.body)
        }
    );

    const data = await response.json();

    res.json(data);
});

export default router;