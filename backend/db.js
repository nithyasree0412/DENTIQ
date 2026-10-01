
import mongoose from 'mongoose';


// =========================
// USER
// =========================

const userSchema = new mongoose.Schema({

    username: {
        type: String,
        required: true,
        unique: true
    },

    password: {
        type: String,
        required: true
    },

    currentStreak: {
        type: Number,
        default: 0
    },

    longestStreak: {
        type: Number,
        default: 0
    },

    lastActiveDate: {
        type: Date,
        default: null
    },
    role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
}
});


// =========================
// SUBJECT
// =========================

const subjectSchema = new mongoose.Schema({

    name: {
        type: String,
        required: true,
        unique: true
    },

    pdfUrl: {
        type: String,
        required: true
    }
});


// =========================
// TEST
// =========================

const testSchema = new mongoose.Schema({

    subjectId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Subject',
        required: true
    },

    questions: [
        {
            question: {
                type: String,
                required: true
            },

            options: {
                A: {
                    type: String,
                    required: true
                },

                B: {
                    type: String,
                    required: true
                },

                C: {
                    type: String,
                    required: true
                },

                D: {
                    type: String,
                    required: true
                }
            },

            answer: {
                type: String,
                required: true,
                enum: ['A', 'B', 'C', 'D']
            }
        }
    ]

}, {
    timestamps: true
});


// =========================
// TEST ATTEMPT
// =========================

const testAttemptSchema = new mongoose.Schema({

    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },

    testId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Test',
        required: true
    },

    subjectId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Subject',
        required: true
    },

    answers: {
        type: Map,
        of: String
    },

    score: {
        type: Number,
        required: true
    },

    totalQuestions: {
        type: Number,
        required: true
    }

}, {
    timestamps: true
});


// =========================
// MODELS
// =========================

const User = mongoose.model(
    'User',
    userSchema
);

const Subject = mongoose.model(
    'Subject',
    subjectSchema
);

const Test = mongoose.model(
    'Test',
    testSchema
);

const TestAttempt = mongoose.model(
    'TestAttempt',
    testAttemptSchema
);


// =========================
// EXPORTS
// =========================

export {
    User,
    Subject,
    Test,
    TestAttempt
};

