import { GitHubButtonIcon } from '@/components/atoms/IconButton'
import Container from '@/components/containers'
import Link from 'next/link'
import Box from '@/components/layouts/Box'
import Flex from '@/components/layouts/Flex'
import Text from '@/components/atoms/Text'

const Footer = () => {
  return (
    <footer>
      <Flex>
        <Box>
          <nav>
            <Box>
              <Link href="/" passHref>TOP</Link>
            </Box>
            {/* <Box minWidth={{ base: '100%', md: '120px' }}>
              <GitHubButtonIcon />
            </Box> */}
          </nav>
        </Box>
      </Flex >
      <Box>
        <Text>
          {new Date().getFullYear()} Tanico*Kazuyo All rights reserved.
        </Text>
      </Box>
    </footer >
  )
}

export default Footer