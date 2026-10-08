% Signal Lost - GNU Octave/MATLAB challenge
% The target waveform is public. Recover the text represented by its segments.

clear;
clc;

target_signal;

fprintf('Signal Lost\n');
fprintf('The target contains %d samples. Enter a candidate flag.\n', numel(target_signal));
candidate = input('flag> ', 's');

candidate_signal = encode_message(candidate, samples_per_symbol);
if numel(candidate_signal) ~= numel(target_signal)
    fprintf('Rejected: wrong number of symbols.\n');
    return;
end

distance = norm(candidate_signal - target_signal);
fprintf('waveform distance: %.12g\n', distance);

if distance < 1e-10
    fprintf('Accepted. The signal is coherent.\n');
else
    fprintf('Rejected. The signal does not match.\n');
end

function signal = encode_message(message, samples_per_symbol)
  % Each character becomes a constant-amplitude segment. The amplitude is
  % whitened with a fixed XOR mask before normalization.
  raw = uint8(message);
  encoded = bitxor(raw, uint8(42));
  amplitudes = double(encoded) / 255;
  signal = reshape(repmat(amplitudes, samples_per_symbol, 1), 1, []);
end
