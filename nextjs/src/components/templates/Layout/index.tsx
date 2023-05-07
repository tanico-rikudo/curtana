import Header from "@/components/orgnisms/Header";
import Footer from "@/components/orgnisms/Footer";
import Separator from "@/components/atoms/Separator";
import Box from "@/components/layouts/Box";


interface LayoutProps {
    children: React.ReactNode
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <>
            <Header />
            <main>{children}</main>
            <Separator />
            <Box>
                <Footer />
            </Box>
        </>
    )
}

export default Layout
