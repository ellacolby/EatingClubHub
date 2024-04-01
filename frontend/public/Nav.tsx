import { memo } from 'react';
import type { FC } from 'react';

import resets from '../_resets.module.css';
import { AkarIconsChevronDownIcon } from './AkarIconsChevronDownIcon';
import classes from './Navs.module.css';

interface Props {
  className?: string;
}
/* @figmaId 31:5 */
export const Navs: FC<Props> = memo(function Navs(props = {}) {
  return (
    <div className={`${resets.storybrainResets} ${classes.root}`}>
      <div className={classes.logo}>
        <div className={classes.eatingClubHub}>EatingClubHub</div>
      </div>
      <div className={classes.navLinks}>
        <div className={classes.home}>Home</div>
        <div className={classes.frame2}>
          <div className={classes.clubs}>Clubs</div>
          <div className={classes.akarIconsChevronDown}>
            <AkarIconsChevronDownIcon className={classes.icon} />
          </div>
        </div>
        <div className={classes.events}>Events</div>
        <div className={classes.contact}>Contact</div>
        <div className={classes.profile}>Profile</div>
      </div>
    </div>
  );
});