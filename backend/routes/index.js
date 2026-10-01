import Router from 'express';
import UserRouter from './user.js'; 
import AIRouter from './ai.js';
import AdminRouter from './admin.js';

import SubjectRouter from './subject.js';

const router = Router();
router.use('/user', UserRouter);
router.use('/ai', AIRouter);
router.use('/subject', SubjectRouter);
router.use('/admin', AdminRouter);
export default router;
