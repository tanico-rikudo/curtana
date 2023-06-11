
import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';
import TextInput from '@/components/atoms/TextInput';
import SelectInput from '@/components/atoms/SelectInput';
import { orderPullBuyBack } from '@/utils/api';
import DateTextInput from '@/components/atoms/DateForm';
import Flex from '@/components/layouts/Flex';


const HeadlineActionForm = (props) => {
    console.log("molecule HeadlineActionForm->index")
    const [buybackDocType, setBuybackDocType] = useState("buyback");
    const [fetchDate, setFetchDate] = useState(new Date());

    const handleBuybackDocType = (newValue: string) => {
        console.log(newValue)
        setBuybackDocType(newValue);
    };

    const hundleFetchDate = (newValue: string) => {
        setFetchDate(newValue);
    };

    function fetchBuyBack() {
        console.log("Call fetch buyback")
        console.log(buybackDocType)

        const year = fetchDate.getFullYear().toString().padStart(4, '0');
        const month = (fetchDate.getMonth() + 1).toString().padStart(2, '0');
        const day = fetchDate.getDate().toString().padStart(2, '0');

        const dateText = year + month + day;
        orderPullBuyBack(dateText, buybackDocType)
    }


    return (
        <>
            <div className="bg-cyan-950 shadow-md rounded my-4 mx-3 py-2 px-1 mb-4">
                {/* <TextInput
                    label="Fetch Date"
                    id=""
                    placeholder='' /> */}
                <Flex class_names='flex flex-row'>
                    <Flex class_names='basis-1/2'>
                        < DateTextInput
                            label="Fetch Date"
                            handleValueChange={hundleFetchDate}
                        />
                    </Flex>
                    <Flex class_names='basis-1/2'>
                        <SelectInput
                            handleValueChange={handleBuybackDocType}
                            label='Select Document Type' >
                            <option selected value="buyback">BuyBack</option>
                            <option value="amend_buyback">Amend BuyBack</option>
                        </SelectInput>
                    </Flex>
                </Flex>
                <Flex class_names='flex flex-row-reverse'>
                    <Flex class_names='basis-full'>
                        <button
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                            onClick={() => fetchBuyBack()}>
                            Fetch
                        </button>
                    </Flex>
                </Flex>
            </div >
        </>
    );
}

export default HeadlineActionForm
