import { ImportExportTwoTone } from "@mui/icons-material"
import Head from "next/head"
import { SITE_NAME, SITE_TITLE, SITE_DESCRIPTION } from "@/lib/constants"

export default function Header() {
  return (
    <Head>
      <meta key="charset" name="charset" content="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      <title key="title">{SITE_TITLE}</title>
      <meta name="title" content={SITE_TITLE} key="meta:title" />
      <meta
        name="description"
        content={SITE_DESCRIPTION}
        key="meta:description"
      />
      <meta property="og:title" content={SITE_TITLE} key="meta:og:title" />
      <meta
        property="og:description"
        content={SITE_DESCRIPTION}
        key="meta:og:description"
      />
      {/* <meta property="og:image" content={`${publicRuntimeConfig.domainUrl}/static/images/icon/icon-512.png`} key="meta:og:image" /> */}
      <meta property="og:site_name" content={SITE_NAME} /> * /
      <meta property="og:locale" content="ja_JP" />
      <meta property="og:type" content="website" />
      <meta property="fb:app_id" content="556485011968079" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@tanico_rikudo" />
    </Head>
  )
}
