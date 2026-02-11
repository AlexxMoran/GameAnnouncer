import { Stepper as MuiStepper, Step, StepLabel } from "@mui/material";
import type { IStepperProps } from "@shared/ui/stepper/types";
import type { FC } from "react";

export const Stepper: FC<IStepperProps> = ({ steps, activeStep, onChangeStep }) => {
  return (
    <MuiStepper activeStep={activeStep} alternativeLabel={false}>
      {steps.map((label, index) => (
        <Step
          key={label}
          index={index}
          sx={{ pl: index === 0 ? 0 : undefined, pr: index === steps.length - 1 ? 0 : undefined }}
        >
          <StepLabel onClick={() => onChangeStep?.(index)}>{label}</StepLabel>
        </Step>
      ))}
    </MuiStepper>
  );
};
