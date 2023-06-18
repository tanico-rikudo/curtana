
import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';

// AG grid requirement
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-balham.css';

// import {
//     ColDef,
//     GridReadyEvent,
//     IDatasource,
//     IGetRowsParams,
// } from 'ag-grid-community';
// import { fetchDetails } from '@/utils/api';


// export default function EdinetDetail(detail) {
const EdinetDetail = ({ details }) => {
    console.log("modelcule detail->index")

    const [columnDefs] = useState([
        { field: 'buy_date', headerName: 'Date', filter: 'agDateColumnFilter' },
        { field: 'buy_qty', headerName: 'Quantity' },
        { field: 'buy_notional', headerName: 'Notional' },
        { field: 'doc_id', headerName: 'Document ID', filter: 'agTextColumnFilter', },
    ]);

    const [defaultColDef] = useState({
        resizable: true,
        sortable: true,
        filter: true,
        floatingFilter: true
    });
    let data = []
    if (details) {
        data = details.details
    }
    console.log(data)

    return (
        <>
            <div className="ag-theme-balham-dark px-4 py-3" style={{ height: '600px' }}>
                <AgGridReact
                    rowData={data}
                    columnDefs={columnDefs}
                ></AgGridReact>
            </div>
        </>
    );
}

export default EdinetDetail
