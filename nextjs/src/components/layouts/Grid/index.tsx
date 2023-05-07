interface GridProps {
  children: React.ReactNode;
  n_mobile_col: number;
  n_sm_col: number;
  n_md_col: number;
  n_lg_col: number;
  n_xl_col: number;
}

const Grid = ({
  children,
  n_mobile_col,
  n_sm_col,
  n_md_col,
  n_lg_col,
  n_xl_col,
}: GridProps) => {
  return (
    <>
      {/* <div className={`grid grid-cols-3 gap-4`} >{children}</div> */}
      <div className={`grid grid-cols-${n_mobile_col} 
      sm:grid-cols-${n_sm_col} 
      md:grid-cols-${n_md_col}
       lg:grid-cols-${n_lg_col}
        xl:grid-cols-${n_xl_col} gap-4`} >{children}</div>

    </>
  );
};

export default Grid;
