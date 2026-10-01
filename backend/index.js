import express from 'express';
import router from './routes/index.js';
import bodyParser from 'body-parser';
import connectDB from './dbs.js';
import cors from 'cors';
import { errorHandler } from './middleware/error.js';
const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use('/api/v1', router);
app.use(errorHandler);
await connectDB();
app.listen(3000, () => {
  console.log('Server is running on port 3000');
} );
