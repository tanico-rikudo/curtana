
import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';

// AG grid requirement
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-balham.css';
import { fetchHeadlines, fetchDetails } from "@/utils/api"
import {
    CellClickedEvent,
    ColDef,
    GridReadyEvent,
    IDatasource,
    IGetRowsParams,
} from 'ag-grid-community';

export interface IDetail {
    id: number,
    doc_id: string,
    buy_qty: number,
    buy_date: number,
    buy_notional: number,
    created_on: Date,
    updated_on: Date,
}


// export default function EdinetHeadline(headline) {
const EdinetHeadline = (props) => {
    console.log("molecule headline->index")

    const [details, setDetail] = useState();
    const [loading, setLoading] = useState(true);
    const gridRef = useRef<AgGridReact<IDetail>>(null);
    const [headlines, setHeadline] = useState();

    const [columnDefs, setColumnDefs] = useState<ColDef[]>([
        {
            field: 'submit_datetime',
            headerName: 'Submit Date',
            filter: 'agDateColumnFilter',
        },
        {
            field: 'doc_id',
            headerName: 'Document ID',
            filter: 'agTextColumnFilter',
        },
        {
            field: 'edinet_code',
            headerName: 'Edinet Code',
            filter: 'agTextColumnFilter',
        },
        {
            field: 'filer_name',
            headerName: 'Filer Name',
            filter: 'agTextColumnFilter',
        },
    ]);

    const defaultColDef = useMemo<ColDef>(() => {
        return {
            resizable: true,
            sortable: true,
            filter: true,
            floatingFilter: true
        };
    }, []);


    const headlineDatasource = {
        async getRows(params: IGetRowsParams) {
            console.log('asking for ' + params.startRow + ' to ' + params.endRow);
            const { startRow, endRow } = params;
            let data = await fetchHeadlines(startRow, endRow)
            data = data.headlines
            console.log(data)
            console.log("got headlines")
            params.successCallback(data, 499)
        }
    };

    const onGridReady = useCallback((params: GridReadyEvent) => {
        // setGridApi(params);
        console.log("Call grid headline")
        // register datasource with the grid
        var dataSource: IDatasource = headlines || headlineDatasource
        // this.gridOptions.dataSource = dataSource
        // console.log(dataSource)
        params.api.setDatasource(dataSource);
    }, []);


    const onSelectionChanged = useCallback(async (event) => {
        const selectedRows = event.api.getSelectedRows();
        setLoading(true);
        let doc_id = selectedRows[0].doc_id
        doc_id = doc_id.trim()
        const details = await fetchDetails(doc_id);
        console.log(details)
        setLoading(false);
        props.handleDetailChange(details);

    }, []);



    return (
        <>
            <div className="ag-theme-balham-dark px-4 py-3" style={{ height: '300px' }}>
                <AgGridReact
                    columnDefs={columnDefs}
                    defaultColDef={defaultColDef}
                    rowBuffer={0}
                    rowSelection={'multiple'}
                    rowModelType={'infinite'}
                    cacheBlockSize={100}
                    cacheOverflowSize={2}
                    maxConcurrentDatasourceRequests={1}
                    infiniteInitialRowCount={200}
                    maxBlocksInCache={10}
                    onGridReady={onGridReady}
                    onSelectionChanged={onSelectionChanged}
                ></AgGridReact>
            </div>
        </>
    );
}

export default EdinetHeadline
