// components/ResearchArea.tsx
import styled from 'styled-components';
import React, { useState, useEffect, useRef } from 'react';
import Venue from './Venue';
import 'font-awesome/css/font-awesome.min.css';

const AreaWrapper = styled.div`
  padding: 10px;
  border-bottom: 1px solid #ccc;
  &:last-child {
    border-bottom: none;
  }
`;

const AreaHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const AreaName = styled.h3`
  margin: 0;
  font-size: 20px;
  display: flex;
  align-items: center;
`;

const ToggleButton = styled.button`
  background-color: #007bff;
  border: none;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  margin-left: 10px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const SubareaWrapper = styled.div`
  margin-left: 20px;
  align-items: center;
  cursor: pointer;
`;

const SubAreaHeader = styled.div`
  display: flex;
  align-items: center;
`;

const SubAreaName = styled.h5`
  margin: 0;
  font-size: 16px;
  display: flex;
  align-items: center;
`;

interface TriangleProps {
  $isOpen: boolean;
}

const Triangle = styled.span<TriangleProps>`
  font-size: 14px;
  margin-right: 8px;
  transform: ${({ $isOpen }) => ($isOpen ? 'rotate(90deg)' : 'rotate(0)')};
  transition: transform 0.3s ease;
`;

interface ResearchAreaProps {
  name: string;
  subareas: { [key: string]: string[] };
  selectedVenues: string[];
  paperCounts: { [venue: string]: number };
  onToggleMajorArea: (areaName: string) => void;
  onToggleMinorArea: (subareaName: string) => void;
  onToggleVenue: (venueName: string) => void;
}

const ResearchArea: React.FC<ResearchAreaProps> = ({ name, subareas, selectedVenues, paperCounts, onToggleMajorArea, onToggleMinorArea, onToggleVenue }) => {
  const [expandedSubareas, setExpandedSubareas] = useState<string[]>([]);
  const checkboxRefs = useRef<{ [key: string]: HTMLInputElement }>({});


  const toggleSubareaExpansion = (subareaName: string) => {
    if (expandedSubareas.includes(subareaName)) {
      setExpandedSubareas(prev => prev.filter(area => area !== subareaName));
    } else {
      setExpandedSubareas(prev => [...prev, subareaName]);
    }
  };

  const isAllSelected = Object.values(subareas).flat().every(conf => selectedVenues.includes(conf));

  const isPartiallySelected = (subareaName: string) => {
    const venues = subareas[subareaName];
    const selectedCount = venues.filter(conf => selectedVenues.includes(conf)).length;
    return selectedCount > 0 && selectedCount < venues.length;
  };

  useEffect(() => {
    Object.keys(subareas).forEach(subareaName => {
      const checkbox = checkboxRefs.current[subareaName];
      if (checkbox) {
        checkbox.indeterminate = isPartiallySelected(subareaName)
      }
    });
  });
  
  return (
    <AreaWrapper>
      <AreaHeader>
        <AreaName> { name } </AreaName>
        <ToggleButton onClick={() => onToggleMajorArea(name)}>
          {isAllSelected ? 'Off' : 'On'}
        </ToggleButton>
      </AreaHeader>
      {Object.keys(subareas).map(subareaName => {
        const venues = subareas[subareaName];
        const isSubareaAllSelected = venues.every(conf => selectedVenues.includes(conf));
        const isSubareaNoneSelected = venues.every(conf => !selectedVenues.includes(conf));
        const isSubareaPartiallySelected = !isSubareaAllSelected && !isSubareaNoneSelected;

        return (
          <SubareaWrapper key={subareaName}>
            <SubAreaHeader>
              <Triangle
                className="fa fa-caret-right"
                $isOpen={expandedSubareas.includes(subareaName)}
                onClick={() => toggleSubareaExpansion(subareaName)}
              />
              <SubAreaName>
                {subareaName}
              </SubAreaName>
              <input
                type="checkbox"
                ref={el => { if (el) { checkboxRefs.current[subareaName] = el } } }
                checked={isSubareaAllSelected}
                onChange={() => onToggleMinorArea(subareaName)}
              />

            </SubAreaHeader>
            {expandedSubareas.includes(subareaName) && venues.map(venue => (
              <Venue
                key={venue}
                name={venue}
                cnt={paperCounts[venue]}
                checked={selectedVenues.includes(venue)}
                onChange={onToggleVenue}
              />
            ))}
          </SubareaWrapper>
        );
      })}
    </AreaWrapper>
  );
};

export default ResearchArea;
