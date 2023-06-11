
interface TextInputProps {
  label: string;
  id: string;
  placeholder: string;
}


export default function TextInput({ label, id, placeholder }: TextInputProps) {
  return (
    <>
      <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0 py-3">
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          {label}
        </label>
        <input className="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
          id={`${id}`}
          type="text"
          placeholder={`${placeholder}`} />
        {/* <p className="text-red-500 text-xs italic">Please fill out this field.</p> */}
      </div>
    </>
  )
}
