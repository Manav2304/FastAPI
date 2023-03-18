import React from "react";
import { gaushala } from "./constant";
import {
  HeadStyle,
  ParagraphStyle,
  ServiceWrapper,
  TextWrapper,
} from "../style";

const mapgaushala = gaushala.map((paragraph) => <p>{paragraph}</p>);
export const Gaushala = () => {
  return (
    <ServiceWrapper>
      <HeadStyle>
        <h1> Goverdhan Gaushala</h1>
      </HeadStyle>
      <TextWrapper>
        <ParagraphStyle>{gaushala}</ParagraphStyle>
      </TextWrapper>
    </ServiceWrapper>
  );
};
