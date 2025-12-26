// components/PaperTable.tsx
import React, { useState } from 'react';
import styled from 'styled-components';
import Paper from '../models/Paper';
import Image from 'next/image';


const TableHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const TableBody = styled.table`
float: left;
   width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 18px;
  text-align: left;
  border-radius: 5px 5px 0 0;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  tr {
    background-color: #f3f3f3;
    color: black;
    border-bottom: 1px solid #ddd;
    &:nth-of-type(even) {
      background-color: #f2f2f2;
    }
    &:last-of-type {
      border-bottom: 2px solid #009879;
    }
  }
  th, td {
    padding: 12px 15px;
    text-align: center;
    &:first-child {
      text-align: left;
    }
  }
  th {
    background-color: #009879;
    color: white;
    border-bottom: none;
  }
`;

const LinkStyle = styled.a`
   color: #009879;
   text-decoration: none;
   font-weight: bold;
   &:hover {
      text-decoration: underline;
   }
`;

interface PaperTableProps {
   papers: Paper[];
}

enum SortBy {
   DATE = 'date',
   STARS = 'stars',
   FORKS = 'forks',
   CITATION = 'citation',
}

const PaperTable: React.FC<PaperTableProps> = ({ papers }) => {
   const [sortBy, setSortBy] = useState<SortBy>(SortBy.DATE);
   const [filterDate, setFilterDate] = useState<string>('');

   const sortPapers = (papers: Paper[]): Paper[] => {
      return papers.sort((a, b) => {
         switch (sortBy) {
            case SortBy.DATE:
               if (a.prioritized && !b.prioritized) {
                  return -1;
               } else if (!a.prioritized && b.prioritized) {
                  return 1;
               }
               return - a.year + b.year;
            case SortBy.STARS:
               return - (a.github_star + (a.repo_name != "" ? 1 : 0)) + (b.github_star + (b.repo_name != "" ? 1 : 0));
            case SortBy.FORKS:
               return - (a.github_fork + (a.repo_name != "" ? 1 : 0)) + (b.github_fork + (b.repo_name != "" ? 1 : 0));
            case SortBy.CITATION:
               return b.citation_count - a.citation_count;
            default:
               return 0;
         }
      });
   };

   const filterPapers = (papers: Paper[]): Paper[] => {
      //       if (filterDate) {
      //          return papers.filter((paper) => paper.date === filterDate);
      //       }
      return papers;
   };

   const displayedPapers = filterPapers(sortPapers([...papers]));

   return (
      <div>
         <TableHeader>
            <div>
               <label>Sort By:</label>
               <select onChange={(e) => setSortBy(e.target.value as SortBy)}>
                  <option value={SortBy.STARS}>Stars</option>
                  <option value={SortBy.FORKS}>forks</option>
                  <option value={SortBy.DATE}>Date</option>
                  <option value={SortBy.CITATION}>Citation</option>
               </select>
            </div>
         </TableHeader>
         <TableBody>
            <thead>
               <tr>
                  <th>Venue</th>
                  <th>Year</th>
                  <th>Paper</th>
                  <th>Artifact</th>
                  <th>Citation</th>
                  <th>Stars</th>
                  <th>Forks</th>
                  <th>Github Issues</th>
                  <th>Last Update</th>
               </tr>
            </thead>
            <tbody>
               {displayedPapers.map((paper, idx) => (
                  <tr key={idx}>
                     <td>{paper.venue}</td>
                     <td>{paper.year}</td>
                     <td>
                        {!paper.paper_link && (<span> {paper.title} </span>)}

                        {paper.paper_link && (<LinkStyle href={paper.paper_link} target="_blank" rel="noopener noreferrer">
                           <span> { paper.title } </span>
                        </LinkStyle>)}
                     </td>
                     <td>
                        {paper.repo_name && (
                           <LinkStyle href={paper.code_link} target="_blank" rel="noopener noreferrer">
                              {paper.repo_name}
                              <Image src="/icons/github-icon.webp" alt="github" width={25} height={25} />
                           </LinkStyle>)}
                     </td>
                     <td>
                        {paper.citation_count}
                     </td>
                     <td>
                        {paper.github_star}
                     </td>
                     <td>
                        {paper.github_fork}
                     </td>
                     <td>
                        {paper.github_issues}
                     </td>
                     <td>
                        {paper.github_update_date}
                     </td>
                  </tr>
               ))}
            </tbody>
         </TableBody>
      </div>
   );
};
export default PaperTable;
