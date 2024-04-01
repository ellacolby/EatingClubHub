import { memo, SVGProps } from 'react';

const AkarIconsChevronDownIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg preserveAspectRatio='none' viewBox='0 0 12 13' fill='none' xmlns='http://www.w3.org/2000/svg' {...props}>
    <path d='M2 5L6 9L10 5' stroke='#FC9114' strokeWidth={1.15} strokeLinecap='round' strokeLinejoin='round' />
  </svg>
);
const Memo = memo(AkarIconsChevronDownIcon);
export { Memo as AkarIconsChevronDownIcon };
