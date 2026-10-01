import Router from 'express';
import { Subject } from '../db.js';

const router = Router();

router.get('/', async (req, res) => {

    const subjects = await Subject.find();

    res.json(subjects);
});

router.get('/:subjectId/modes', async (req, res) => {

    const { subjectId } = req.params;

    res.json({
        subjectId,
        modes: [
            "test",
            "doubt"
        ]
    });
});

export default router;