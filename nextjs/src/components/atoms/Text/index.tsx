interface TextProps {
  children: React.ReactNode;
}

const Text = ({ children }: TextProps) => {
  return (
    <>
      <p className="text-yellow">{children}</p>
    </>
  );
};

export default Text;
