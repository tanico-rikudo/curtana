interface FlexProps {
  children: React.ReactNode
  class_names: string;
}

const Flex = ({ children, class_names }: FlexProps) => {
  return (
    <>
      <div className={`${class_names}`}>{children}</div>
    </>
  )
}

export default Flex