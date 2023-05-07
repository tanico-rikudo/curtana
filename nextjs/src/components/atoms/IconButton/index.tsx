import GithubIcon from '@mui/icons-material/GitHub'
import IconButton from '@mui/material/IconButton';

// function withIconStyle(Icon, size) {
//     return (
//         <IconButton size={size}>
//             <Icon fontSize='inherit' />
//         </IconButton>
//     )

// }
// export const GitHubButtonIcon = (size) => {
//     return withIconStyle(GithubIcon, size)
// }

function Icon() {
    return (
        // <IconButton size='small' >
        <GithubIcon fontSize='inherit' />
        // </IconButton >
    )
}

export const GitHubButtonIcon = Icon