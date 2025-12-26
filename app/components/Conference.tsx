// components/Conference.tsx
import styled from 'styled-components';
import React from 'react';

const ConferenceWrapper = styled.div`
  display: flex;
  align-items: center;
  margin: 5px 0;
`;

const CheckboxLabel = styled.label`
  margin-left: 10px;
  cursor: pointer;
  font-size: 16px;
`;

interface ConferenceProps {
  name: string;
  checked: boolean;
  onChange: (conferenceName: string) => void;
}

const Conference: React.FC<ConferenceProps> = ({ name, checked, onChange }) => {
  return (
    <ConferenceWrapper>
      <CheckboxLabel htmlFor={name}>{name}</CheckboxLabel>
      <input 
        type="checkbox" 
        id={name}
        checked={checked}
        onChange={() => onChange(name)} 
      />
    </ConferenceWrapper>
  );
};


export default Conference;
