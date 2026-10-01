import Router from 'express';
import { User, TestAttempt } from '../db.js';
import bcrypt from 'bcryptjs';
import { signupvalidation, loginvalidation } from '../validations/user.js';
import { generateToken } from '../utils/jwt.js';
import { updateStreak } from '../utils/streak.js';
import { authMiddleware } from '../middleware/auth.js';

const router = Router();

router.post('/signup', async (req, res) => {

    const { success } = signupvalidation.safeParse(req.body);

    if (!success) {
        return res.status(400).json({
            message: "Email already taken / Incorrect inputs"
        });
    }

    const existingUser = await User.findOne({
        username: req.body.username
    });

    if (existingUser) {
        return res.status(400).json({
            message: "Email already taken"
        });
    }

    const hashedPassword = await bcrypt.hash(
        req.body.password,
        12
    );

    const user = new User({
        username: req.body.username,
        password: hashedPassword
    });

    await user.save();

    res.json({
        message: 'user Signup'
    });
});

router.post('/login', async (req, res) => {

    const { success } = loginvalidation.safeParse(req.body);

    if (!success) {
        return res.status(400).json({
            message: "Incorrect inputs"
        });
    }

    const user = await User.findOne({
        username: req.body.username
    });

    if (!user) {
        return res.status(400).json({
            message: "Error while logging in"
        });
    }

    const passwordMatch = await bcrypt.compare(
        req.body.password,
        user.password
    );

    if (!passwordMatch) {
        return res.status(400).json({
            message: "password Error while logging in"
        });
    }

    const streakUpdated = updateStreak(user);

    if (streakUpdated) {
        await user.save();
    }

    const userId = user._id;

    const token = generateToken(
        userId,
        user.role
    );

    res.json({
        message: 'user Login',
        token
    });
});

router.get('/dashboard', authMiddleware, async (req, res) => {

    const user = await User.findById(req.userId);

    const attempts = await TestAttempt
        .find({ userId: req.userId })
        .populate('subjectId', 'name')
        .sort({ createdAt: -1 })
        .limit(10);

    const recentAttempts = attempts.map((attempt) => ({
        attemptId: attempt._id,
        subjectName: attempt.subjectId.name,
        score: attempt.score,
        totalQuestions: attempt.totalQuestions,
        attemptedAt: attempt.createdAt
    }));

    res.json({
        currentStreak: user.currentStreak,
        longestStreak: user.longestStreak,
        recentAttempts
    });
});

export default router;