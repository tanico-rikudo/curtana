import Grid from "@/components/layouts/Grid";

interface PostCardListProps {
  n_mobile_col: number;
  n_sm_col: number;
  n_md_col: number;
  n_lg_col: number;
  n_xl_col: number;
}

const PostCardList = ({
  n_mobile_col = 1,
  n_sm_col = 1,
  n_md_col = 4,
  n_lg_col = 4,
  n_xl_col = 5,
  children,
}: React.PropsWithChildren<PostCardListProps>) => {
  return <Grid
    n_mobile_col={n_mobile_col}
    n_sm_col={n_sm_col}
    n_md_col={n_md_col}
    n_lg_col={n_lg_col}
    n_xl_col={n_xl_col}
  > {children}</Grid>;
};

export default PostCardList;
