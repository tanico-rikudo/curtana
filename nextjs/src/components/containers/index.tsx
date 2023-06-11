import { ReactElement } from 'react';

interface ContainerProps {
  children: ReactElement
}

export default function Container({ children }: ContainerProps) {
  return (
    <div className="container mx-auto">{children}</div>
  )
}
