
import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';

// AG grid requirement
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-balham.css';

import {
    ColDef,
    GridReadyEvent,
    IDatasource,
    IGetRowsParams,
} from 'ag-grid-community';


// export default function EdinetDetail(detail) {
const EdinetDetail = () => {
    console.log("modelcule detail->index")

    const [columnDefs, setColumnDefs] = useState<ColDef[]>([
        { field: 'buy_date', headerName: 'Date', filter: 'agDateColumnFilter' },
        { field: 'buy_qty', headerName: 'Quantity' },
        { field: 'buy_notional', headerName: 'Notional' },
        { field: 'doc_id', headerName: 'Document ID', filter: 'agTextColumnFilter', },
    ]);

    const detailDatasource = {
        getRows(params: IGetRowsParams) {
            setTimeout(function () {
                console.log('asking for ' + params.startRow + ' to ' + params.endRow);
                const { startRow, endRow } = params;
                const promise = fetch('api/detail?startRow=' + startRow + '&endRow=' + endRow, { method: 'GET' })
                promise.then(response => {
                    // レスポンスステータスのチェック。200以外でもresponseが返ればここへ来る。ネットワークエラー等の場合、then()にはこないでcatch()へ行く。
                    if (response.status !== 200) {
                        // 200以外ならばエラーメッセージを投げる
                        throw `response.status = ${response.status}, response.statusText = ${response.statusText}`;
                    }
                    return response.json(); // jsonデータの取得結果をPromiseで返す。
                }).then(response => {
                    response = response.details
                    params.successCallback(response, 499);
                }).catch(err => {
                    console.log(err);
                    params.failCallback();
                });
            }, 500);
        }
    };

    const onGridReady = useCallback((params: GridReadyEvent) => {
        // setGridApi(params);
        console.log("Callgr")
        // register datasource with the grid
        var dataSource: IDatasource = detailDatasource
        // this.gridOptions.dataSource = dataSource
        params.api.setDatasource(dataSource);
    }, []);

    const defaultColDef = useMemo<ColDef>(() => {
        return {
            resizable: true,
            sortable: true,
            filter: true,
            floatingFilter: true
        };
    }, []);

    return (
        <>
            <div className="ag-theme-balham-dark" style={{ height: '600px' }}>
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
                ></AgGridReact>
            </div>
        </>
    );
}

export default EdinetDetail
