import {z} from 'zod';

export const signupvalidation    = z.object({
    username: z.string().email(),
    password: z.string()
    
})
export const loginvalidation = z.object({
    username: z.string().email(),
    password: z.string()
})
