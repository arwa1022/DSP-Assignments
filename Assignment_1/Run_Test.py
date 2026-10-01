from DSP_Assignment_1 import ReadSignalFile, addSignals, subtractSignals, multiplySignalByConst, advance, folding
from DSP_Task_Test_Functions import AddSignalSamplesAreEqual, SubSignalSamplesAreEqual, MultiplySignalByConst, ShiftSignalByConst, Folding



ind1, samp1 = ReadSignalFile("input_signals/Signal1.txt")
ind2, samp2 = ReadSignalFile("input_signals/Signal2.txt")


add_ind, add_samp = addSignals(ind1, samp1, ind2, samp2)
AddSignalSamplesAreEqual("input_signals/Signal1.txt", "input_signals/Signal2.txt", add_ind, add_samp)

sub_ind, sub_samp = subtractSignals(ind1, samp1, ind2, samp2)
SubSignalSamplesAreEqual("input_signals/Signal1.txt", "input_signals/Signal2.txt", sub_ind, sub_samp)

mul_ind, mul_samp = multiplySignalByConst(ind1, samp1, 5)
MultiplySignalByConst(5, mul_ind, mul_samp)

shift_ind, shift_samp = advance(ind1, samp1, 3)
ShiftSignalByConst(3, shift_ind, shift_samp)

fold_ind, fold_samp = folding(ind1, samp1)
Folding(fold_ind, fold_samp)