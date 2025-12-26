// components/Sidebar.tsx
import React from 'react';
import styled from 'styled-components';
import Image from 'next/image';
import ResearchArea from './ResearchArea';

const SidebarWrapper = styled.div`
  margin: 20px 0;
  background-color: #f3f3f3; // Light gray background, consistent with the table rows.
  border-radius: 5px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); // Same shadow as the table.
  margin-right: 20px; // Space between the sidebar and the table.
`;

interface SidebarProps {
  areas: { [key: string]: { [subkey: string]: string[] } }; // Updated structure
  selectedVenues: string[];
  paperCounts: { [venue: string]: number };
  onToggleMajorArea: (areaName: string) => void; // New handler
  onToggleMinorArea: (subareaName: string) => void; // New handler
  onToggleVenue: (venueName: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ areas, selectedVenues, paperCounts, onToggleMajorArea, onToggleMinorArea, onToggleVenue }) => {
  return (
    <SidebarWrapper>
      {Object.keys(areas).map(areaName => (
        <ResearchArea
          key={areaName}
          name={areaName}
          paperCounts={paperCounts}
          subareas={areas[areaName]} // Pass the subareas instead of just venues
          selectedVenues={selectedVenues}
          onToggleMajorArea={onToggleMajorArea}
          onToggleMinorArea={onToggleMinorArea} // Passing the new handler for minor areas
          onToggleVenue={onToggleVenue}
        />
      ))}
      <p>
        <a href="/original_papers.json" download style={{ display: 'block', margin: '10px 0' }}>Click here to download the dataset we used in our paper.</a>
      </p>
      <p>
        <a href="/papers.json" download style={{ display: 'block', margin: '10px 0' }}>Click here to download the dataset used in this website.</a>
      </p>
      <p>
        <a href="https://github.com/morgen52/SE-artifact">Our GitHub repository
        <Image src="/icons/github-icon.webp" alt="github" width={25} height={25} />
        </a>
      </p>

      <p>
        if you use this dataset, please cite our paper.
      </p>

      <p>
        <span style={{ display: 'block', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            {`@article{
  LIU2024112032,
  title = {Research artifacts in software engineering publications: Status and trends},
  journal = {Journal of Systems and Software},
  volume = {213},
  pages = {112032},
  year = {2024},
  issn = {0164-1212},
  doi = {https://doi.org/10.1016/j.jss.2024.112032},
  author = {Mugeng Liu and Xiaolong Huang and Wei He and Yibing Xie and Jie M. Zhang and Xiang Jing and Zhenpeng Chen and Yun Ma} }`}
        </span>
      </p>
    </SidebarWrapper>
  );
};

export default Sidebar;
