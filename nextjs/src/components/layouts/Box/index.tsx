interface BoxProps {
  children: React.ReactNode
}

const Box = ({ children }: BoxProps) => {
  return (
    <>
      <div className="box-content">{children}</div>
    </>
  )
}

export default Box