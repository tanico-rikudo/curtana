
interface SelectInputProps {
  label: string;
  handleValueChange: any;
  children: React.ReactNode;
}

export default function SelectInput({ label, handleValueChange, children }: SelectInputProps) {

  const handleInputChange = (event) => {
    const value = event.target.value;
    console.log("Call change select option")
    handleValueChange(value);
  };

  return (
    <>
      <div className="w-full px-3 mb-6 md:mb-0 py-3">
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          {label}
        </label>
        <select onChange={handleInputChange} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          {children}
        </select>
      </div>
    </>
  )
}
