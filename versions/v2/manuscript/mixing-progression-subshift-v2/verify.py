import itertools
import json
import math


def legal_support(support):
    if not support:
        return True
    maximum = max(support)
    difference = 1
    while (difference * difference + 2) * difference <= maximum:
        length = difference * difference + 3
        for start in support:
            if start + (length - 1) * difference <= maximum:
                if all(start + offset * difference in support for offset in range(length)):
                    return False
        difference += 1
    return True


def quarter_mask(coordinate, denominator, lower_eighth):
    floor_phase = math.isqrt(2 * coordinate * coordinate) // denominator
    lower = denominator * (8 * floor_phase + lower_eighth)
    upper = denominator * (8 * floor_phase + lower_eighth + 2)
    squared_phase = 128 * coordinate * coordinate
    return lower * lower <= squared_phase <= upper * upper


def legal_support_with_length(support, progression_length):
    if not support:
        return True
    maximum = max(support)
    for difference in range(1, maximum + 1):
        length = progression_length(difference)
        for start in support:
            if start + (length - 1) * difference <= maximum:
                if all(start + offset * difference in support for offset in range(length)):
                    return False
    return True


def main():
    words = []
    for length in range(6):
        for bits in itertools.product((0, 1), repeat=length):
            support = {index for index, value in enumerate(bits) if value}
            if legal_support(support):
                words.append((length, support))
    joining_count = 0
    for left_length, left_support in words:
        for right_length, right_support in words:
            threshold = left_length + max(left_length, right_length)
            for start in range(threshold, threshold + 3):
                support = left_support | {start + index for index in right_support}
                assert legal_support(support)
                joining_count += 1

    mask_windows = 0
    for radius in range(21):
        denominator = 32 * (radius + 1)
        masks = [
            {coordinate for coordinate in range(4021)
             if quarter_mask(coordinate, denominator, lower)}
            for lower in (1, 5)
        ]
        assert all(coordinate not in masks[0] | masks[1]
                   for coordinate in range(radius + 1))
        for start in range(4001):
            window = set(range(start, start + radius + 1))
            assert not (window & masks[0] and window & masks[1])
            mask_windows += 1

    norm_instances = 0
    for denominator in (32, 64, 96, 128, 160, 192):
        for multiplier in range(1, 1001):
            floor_phase = math.isqrt(2 * multiplier * multiplier) // denominator
            nearest = floor_phase + (
                8 * multiplier * multiplier
                >= denominator * denominator * (2 * floor_phase + 1) ** 2)
            norm = 2 * multiplier * multiplier - denominator * denominator * nearest * nearest
            assert norm != 0
            upper = (denominator + 3) * multiplier - denominator * nearest
            assert upper > 0 and upper * upper >= 2 * multiplier * multiplier
            norm_instances += 1

    rotation_instances = 0
    largest_hitting_index = 0
    for denominator in (32, 64, 96):
        bound_constant = 256 * denominator * (denominator + 3)
        for difference in range(1, 81):
            for start in (0, 1, 17, 100):
                for lower_eighth in (1, 5):
                    for offset in range(100001):
                        if quarter_mask(start + offset * difference, denominator, lower_eighth):
                            assert offset <= bound_constant * difference
                            largest_hitting_index = max(largest_hitting_index, offset)
                            break
                    else:
                        raise AssertionError('Finite rotation bound exceeded')
                    rotation_instances += 1

    obstruction_fillings = 0
    for difference in range(1, 11):
        length = difference * difference + 3
        left_support = {index * difference for index in range(length - 1)}
        assert legal_support(left_support)
        word_length = (length - 2) * difference + 1
        gap = difference - 1
        for filler in itertools.product((0, 1), repeat=gap):
            support = left_support | {word_length + index
                                      for index, value in enumerate(filler) if value}
            support.add(word_length + gap)
            assert all(index * difference in support for index in range(length))
            obstruction_fillings += 1

    singleton_cycles = 0
    for period in range(2, 21):
        locations = [(-time) % period for time in range(period + 1)]
        for time in range(period):
            if locations[time] > 0:
                assert locations[time] - 1 == locations[time + 1]
            else:
                assert locations[time + 1] == period - 1
        assert all((index * period) % period == 0
                   for index in range(period * period + 3))
        singleton_cycles += 1

    syndetic_instances = 0
    for radius in range(21):
        denominator = 32 * (radius + 1)
        bound_constant = 256 * denominator * (denominator + 3)
        for start in (0, 1, 17, 100, 1000):
            for target_eighth, erased_eighth in ((4, 1), (0, 5)):
                for offset in range(2 * denominator + 1):
                    if quarter_mask(start + offset, denominator, target_eighth):
                        assert offset <= bound_constant
                        assert all(not quarter_mask(start + offset + index,
                                                    denominator, erased_eighth)
                                   for index in range(radius + 1))
                        break
                else:
                    raise AssertionError('Quarter-interval instance exceeded its finite search range')
                syndetic_instances += 1

    general_obstructions = 0
    length_functions = {
        'quadratic': lambda difference: difference * difference + 3,
        'three_halves': lambda difference: math.isqrt(difference ** 3) + 4,
        'nonmonotone_quadratic': lambda difference:
            difference * difference * (1 if difference % 2 == 0 else 9) + 3,
    }
    for progression_length in length_functions.values():
        for base in range(1, 5):
            difference = min((base * multiplier for multiplier in range(1, 5)),
                             key=progression_length)
            length = progression_length(difference)
            support = {index * difference for index in range(length - 1)}
            assert legal_support_with_length(support, progression_length)
            assert legal_support_with_length({difference - 1}, progression_length)
            word_length = (length - 2) * difference + 1
            for filler in itertools.product((0, 1), repeat=difference - 1):
                combined = support | {word_length + index for index, value
                                      in enumerate(filler) if value}
                combined.add(word_length + difference - 1)
                assert all(index * difference in combined for index in range(length))
                general_obstructions += 1

    print(json.dumps({
        'schema_version': 1,
        'arithmetic': 'exact integers; square-root comparisons by integer squares',
        'joining': {'maximum_prefix_length': 5, 'legal_words': len(words),
                    'placements_beyond_threshold': 3, 'instances': joining_count},
        'separated_masks': {'radius_min': 0, 'radius_max': 20,
                            'window_start_min': 0, 'window_start_max': 4000,
                            'instances': mask_windows},
        'integer_norm_bound': {'denominators': [32, 64, 96, 128, 160, 192],
                               'multiplier_min': 1, 'multiplier_max': 1000,
                               'instances': norm_instances},
        'quarter_interval_hitting': {'denominators': [32, 64, 96],
                                     'difference_min': 1, 'difference_max': 80,
                                     'starting_coordinates': [0, 1, 17, 100],
                                     'instances': rotation_instances,
                                     'largest_hitting_index': largest_hitting_index},
        'quasi_finite_type_obstruction': {'difference_min': 1, 'difference_max': 10,
                                         'all_binary_fillings': obstruction_fillings},
        'singleton_pseudo_orbits': {'period_min': 2, 'period_max': 20,
                                    'instances': singleton_cycles},
        'syndetic_tracing_intervals': {'radius_min': 0, 'radius_max': 20,
                                      'starting_coordinates': [0, 1, 17, 100, 1000],
                                      'instances': syndetic_instances},
        'general_length_obstructions': {'families': list(length_functions),
                                        'base_min': 1, 'base_max': 4,
                                        'binary_fillings': general_obstructions},
        'status': 'pass',
        'scope': 'Finite instances; infinite statements have written proofs in note.tex.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
