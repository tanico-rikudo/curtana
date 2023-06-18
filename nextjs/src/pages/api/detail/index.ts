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
        let { startRow, endRow, doc_id } = req.query as unknown as {
            startRow: string;
            endRow: string;
            doc_id: string;
        };

        let startRowInt = parseInt(startRow)
        let endRowInt = parseInt(endRow)
        startRowInt = startRowInt || 0
        endRowInt = endRowInt || 1000

        const details = await prisma.buyback_detail.findMany({
            // take: endRowInt - startRowInt,
            // skip: startRowInt,
            where: {
                doc_id: {
                    contains: doc_id
                },
            }
        })
        return res.status(200).json({ details });
    }
}