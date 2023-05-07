import prisma from '@/lib/prisma';
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
        methods: ['GET'],
        origin: '*',
        optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
    });
    console.log("api")
    if (req.method == 'GET') {
        let { startRow, endRow } = req.query as unknown as {
            startRow: string;
            endRow: string;
        };
        const startRowInt = parseInt(startRow)
        const endRowInt = parseInt(endRow)

        const headlines = await prisma.buyback_headline.findMany({
            take: endRowInt - startRowInt,
            skip: startRowInt
        })
        return res.status(200).json({ headlines });
    }
}