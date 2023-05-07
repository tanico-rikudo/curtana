interface FlexProps {
  children: React.ReactNode
}

const Flex = ({ children }: FlexProps) => {
  return (
    <>
      <div className="flex-initial w-32">{children}</div>
    </>
  )
}

export default Flex