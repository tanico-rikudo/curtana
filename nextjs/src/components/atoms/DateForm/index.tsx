
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css"

interface DateTextInputProps {
  label: string;
  handleValueChange: any;
  id: string;
  placeholder: string;
}


export default function DateTextInput({ label, handleValueChange, id, placeholder }: DateTextInputProps) {

  const [startDate, setStartDate] = useState(new Date());
  handleValueChange(startDate)


  const handleInputChange = (date) => {
    setStartDate(date);
    handleValueChange(date);
  };


  return (
    <>
      <div className="w-full px-3 mb-6 md:mb-0 py-3">
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          {label}
        </label>
        <DatePicker
          className="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
          dateFormat="yyyyMMdd"
          // locale="ja"
          selected={startDate}
          onChange={(date) => handleInputChange(date)} />
        {/* <p className="text-red-500 text-xs italic">Please fill out this field.</p> */}
      </div>
    </>
  )
}
