% Organizer-only helper. Run this once to create target_signal.m.
% Keep the generated target_signal.m as the challenge attachment.

flag = 'SecurinetsENIT{fft_reveals_the_message}';
samples_per_symbol = 32;
raw = uint8(flag);
encoded = bitxor(raw, uint8(42));
amplitudes = double(encoded) / 255;
target_signal = reshape(repmat(amplitudes, samples_per_symbol, 1), 1, []);

fid = fopen('target_signal.m', 'w');
fprintf(fid, 'samples_per_symbol = %d;\n', samples_per_symbol);
fprintf(fid, 'target_signal = [\n');
fprintf(fid, '%.17g ', target_signal);
fprintf(fid, '];\n');
fclose(fid);
