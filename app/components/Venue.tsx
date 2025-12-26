// components/Venue.tsx
import styled from 'styled-components';
import React from 'react';

const VenueWrapper = styled.div`
  display: flex;
  align-items: center;
  margin: 5px 0;
`;

const CheckboxLabel = styled.label`
  margin-left: 10px;
  cursor: pointer;
  font-size: 16px;
`;

interface VenueProps {
  name: string;
  checked: boolean;
  cnt: number;
  onChange: (venueName: string) => void;
}

const Venue: React.FC<VenueProps> = ({ name, cnt, checked, onChange }) => {
  return (
    <VenueWrapper>
      <CheckboxLabel htmlFor={name}>{name} ({cnt})</CheckboxLabel>
      <input 
        type="checkbox" 
        id={name}
        checked={checked}
        onChange={() => onChange(name)} 
      />
    </VenueWrapper>
  );
};


export default Venue;
