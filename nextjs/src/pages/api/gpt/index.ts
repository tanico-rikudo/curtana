// import { OpenaiService } from '@/services/openai-service';
import { Configuration, OpenAIApi } from 'openai';
import { NextResponse } from 'next/server';
import { NextApiRequest, NextApiResponse } from 'next';
import NextCors from 'nextjs-cors';

type Data = {
    name: string
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {

    await NextCors(req, res, {
        // Options
        methods: ['POST'],
        origin: '*',
        optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
    });
    console.log("chat gpt api")
    if (req.method == 'POST') {
        const { prompt } = req.body;

        if (!prompt || prompt === '') {
            res.status(400).json({
                message:
                    { content: 'Prompt is required' }
            })
        };


        const configuration = new Configuration({
            apiKey: "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",
        });
        const instance = new OpenAIApi(configuration);
        console.log(prompt)
        const response = await instance.createChatCompletion({
            model: 'gpt-3.5-turbo',
            temperature: 0.9,
            max_tokens: 2048,
            frequency_penalty: 0.5,
            presence_penalty: 0,
            messages: [{ role: 'user', content: prompt }],
        });
        if (response.status !== 200) {
            console.log(`status = ${response.status} : `, response.statusText);
            res.status(400).json({
                message:
                    { content: 'Something error' }
            })
        }
        const message = response.data.choices[0].message || 'Sorry, there was an error.';
        return res.status(200).send({ message: message });
    }
}
