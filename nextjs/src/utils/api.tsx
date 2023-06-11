export const fetchDetails = async (doc_id) => {
    const data = await fetchWithTimeout('api/detail?doc_id=' + doc_id, 1000)
        .then(data => {
            return data.json()
        })
        .catch((reason) => console.error(reason));
    console.log("doc id=" + doc_id + ". ")
    console.log(data)

    return data
}

export const fetchHeadlines = async (startRow, endRow) => {
    const data = await fetchWithTimeout('api/headline?startRow=' + startRow + '&endRow=' + endRow, 1000)
        .then(data => {
            return data.json()
        })
        .catch((reason) => console.error(reason));
    return data
}

export const orderPullBuyBack = async (date, doc_type) => {
    // let d = new Date();
    // http://localhost:8000/headlines/fetch?doc_type=buyback&date=20230612
    // const date = d.getFullYear().toString().padStart(2, '0') + (1 + d.getMonth()).toString().padStart(2, '0') + (d.getDate() - 1).toString().padStart(2, '0')
    console.log("Pull Api called")
    const data = await fetchWithTimeout(`http://localhost:8000/headlines/fetch?doc_type=${doc_type}&date=${date}`, 1000)
        .then(data => {
            return data
        })
        .catch((reason) => console.error(reason));
    return data
}

const fetchWithTimeout = async (url: string, ms: number) => {
    const controller = new AbortController();
    setTimeout(() => controller.abort(), ms);
    console.log("fetch time out func")
    const data = await attemptFetch(url, controller.signal).catch(e => {
        if (e instanceof DOMException && e.name === 'AbortError') {
            throw new Error('Fetch timeout');
        }
        throw e;
    });
    return data
};


const attemptFetch = (url: string, signal?: AbortSignal) =>
    fetch(url, { signal })
        .then(response => {
            if (response.ok) {
                return response;
            } else {
                throw new Error(`Invalid Response: ${response.status}`);
            }
        });