import Router from 'express';
import multer from 'multer';
import { adminMiddleware } from '../middleware/admin.js';
import { authMiddleware } from '../middleware/auth.js';
import { Subject } from '../db.js';

const router = Router();

const upload = multer({
    dest: '../data/pdfs/'
});

router.post(
    '/subject',
    authMiddleware,
    adminMiddleware,
    upload.single('pdf'),
    async (req, res) => {

        const subjectName = req.body.subjectName;
        const pdfPath = req.file.path;

        const subject = await Subject.create({
            name: subjectName,
            pdfUrl: pdfPath
        });

        const response = await fetch(
            'http://localhost:8000/api/v1/rag/ingest',
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    pdfPath: pdfPath,
                    subjectId: subject._id.toString(),
                    subjectName: subject.name
                })
            }
        );

        const data = await response.json();

        res.json({
            message: "Subject added successfully",
            subject: subject,
            ai: data
        });
    }
);

export default router;