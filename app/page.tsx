"use client"

// app/pages/index.tsx
import React, { useState, useEffect } from 'react';
import Paper from './models/Paper'
import Sidebar from './components/Sidebar';
import PaperTable from './components/PaperTable';
import styled from 'styled-components';
import Head from 'next/head';

type ResearchAreas = {
  [key: string]: {
   [key: string]: string[];
  }
};

const HeaderContainer = styled.header`
  text-align: center;
  margin: 10px 0;
  font-size: 24px;
  font-weight: bold;
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: bold;
  margin: 20px 0;
`;

const Divider = styled.hr`
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
`;

const Header: React.FC = () => {
  return (
    <HeaderContainer>
      <Title>CS-Artifacts</Title>
      <Divider />
    </HeaderContainer>
  );
};

const Container = styled.div`
  display: flex;
  align-items: flex-start;
`;

const SidebarWrapper = styled.div`
  flex: 0 0 20%; /* This gives the sidebar a fixed width of 20% */
  padding-right: 20px; // Adjust for spacing between sidebar and table
`;

const TableWrapper = styled.div`
  flex: 1; /* This allows the table to take up the remaining width */
`;


const getAllVenues = (areas: ResearchAreas) => {
  return Object.values(areas).flatMap(area =>
    Object.values(area).flatMap(venues => venues)
  );
};


const countPapersByVenue = (papers: Paper[], allVenues: string[]): { [venue: string]: number } => {
  const venueCounts: { [venue: string]: number } = {};

  // Initialize counts for all venues to 0
  allVenues.forEach(venue => {
    venueCounts[venue] = 0;
  });

  // Increment counts based on papers
  papers.forEach(paper => {
    if (venueCounts.hasOwnProperty(paper.venue)) {
      venueCounts[paper.venue] += 1;
    }
  });

  return venueCounts;
};



const Home: React.FC = () => {
   const [papers, setPapers] = useState<Paper[]>([]);
   const areas : ResearchAreas = {
   'AI': {
      'Computer vision': ['AAAI', 'IJCAI'],
      'Artificial intelligence': ['CVPR', 'ECCV', 'ICCV'],
      'Machine learning': ['ICLR', 'ICML', 'NeurIPS']
   },
   'Systems': {
      'Computer networks': ['SIGCOMM', 'NSDI', 'TON'],
      'Computer security': ['CCS', 'IEEE S&P', 'USENIX Security'],
      'Databases': ['SIGMOD', 'VLDB'],
      'Operating systems': ['OSDI', 'SOSP', 'TOCS'],
      'Programming languages': ['PLDI', 'POPL'],
      'Software engineering': ['FSE', 'ICSE', 'ASE', 'ISSTA', 'JSS', 'ICSME']
   }
   };
   const allVenues = getAllVenues(areas)
   const paperCounts = countPapersByVenue(papers, allVenues);

   const [selectedVenues, setSelectedVenues] = useState<string[]>(getAllVenues(areas));

   useEffect(() => {
      const data = require('../data/papers.json');
      setPapers(data);
   }, []);


   const handleToggleMajorArea = (areaName: string) => {
   const venues = Object.values(areas[areaName]).flat();
   if (venues.every(conf => selectedVenues.includes(conf))) {
      setSelectedVenues(prev => prev.filter(conf => !venues.includes(conf)));
   } else {
      setSelectedVenues(prev => [...prev, ...venues]);
   }
   };

   const handleToggleMinorArea = (subareaName: string) => {
   const venues = Object.values(areas).find(subareas => subareas.hasOwnProperty(subareaName))![subareaName];
   if (venues.every(conf => selectedVenues.includes(conf))) {
      setSelectedVenues(prev => prev.filter(conf => !venues.includes(conf)));
   } else {
      setSelectedVenues(prev => [...prev, ...venues]);
   }
   };

// Pass these handlers to the <Sidebar /> component

   const handleToggleVenue = (venueName: string) => {
      if (selectedVenues.includes(venueName)) {
         setSelectedVenues(prev => prev.filter(conf => conf !== venueName));
      } else {
         setSelectedVenues(prev => [...prev, venueName]);
      }
   };

   const filteredPapers = papers.filter((paper) => selectedVenues.includes(paper.venue));

   return (
      <>
         <Head>
            <title>CS-Artifacts</title>
         </Head>
         <div>
            <Header />
            <Container>
               <SidebarWrapper>
                  <Sidebar
                     paperCounts={paperCounts}
                     areas={areas}
                     selectedVenues={selectedVenues}
                     onToggleMajorArea={handleToggleMajorArea}
                     onToggleMinorArea={handleToggleMinorArea}
                     onToggleVenue={handleToggleVenue}
                  />
               </SidebarWrapper>
               <TableWrapper>
                  <PaperTable papers={filteredPapers} />
               </TableWrapper>
            </Container>
         </div>
      </>
   );
};

export default Home;
