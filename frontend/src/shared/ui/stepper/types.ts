export interface IStepperProps {
  steps: string[];
  activeStep: number;
  onChangeStep?: (step: number) => void;
}
