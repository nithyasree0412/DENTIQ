import mongoose from 'mongoose';

import connectDB from './dbs.js';
import { Subject } from './db.js';

await connectDB();

const existingSubject = await Subject.findOne({
    name: 'Computer Networks'
});

if (!existingSubject) {

    await Subject.create({
        name: 'Computer Networks',
        pdfUrl: 'C:\\Users\\adhit\\OneDrive\\prof_ethics\\PROJECT\\data\\pdfs\\top_down approach book.pdf'
    });

   

} 

await mongoose.connection.close();