from cartoonify import *


def test_separate_channels():
    assert separate_channels([[[1, 2]]]) == [[[1]], [[2]]]
    assert separate_channels([[[1]]]) == [[[1]]]
    assert separate_channels([[[1, 2], [1, 2]]]) == [[[1, 1]], [[2, 2]]]
    assert separate_channels([[[1, 2]], [[1, 2]]]) == [[[1], [1]], [[2], [2]]]
    assert separate_channels([[[1, 2, 3]]]) == [[[1]], [[2]], [[3]]]
    assert separate_channels([[[1, 2], [3, 4]]]) == [[[1, 3]], [[2, 4]]]
    assert separate_channels([[[1, 2]], [[3, 4]]]) == [[[1], [3]], [[2], [4]]]
    assert separate_channels([[[1, 2, 3], [1, 2, 3]], [[0, 9, 8], [0, 9, 8]]]) == [[[1, 1], [0, 0]],[[2, 2],[9,9]],
                                                                                    [[3, 3], [8, 8]]]
    assert separate_channels(
        [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]) == [
               [[1, 4], [7, 10]], [[2, 5], [8, 11]], [[3, 6], [9, 12]]]
    assert separate_channels(
        [[[1, 2, 3], [1, 2, 3]], [[4, 5, 6], [4, 5, 6]], [[7, 8, 9], [7, 8, 9]], [[10, 11, 12], [10, 11, 12]]]
    ) == [[[1, 1], [4, 4], [7, 7], [10, 10]], [[2, 2], [5, 5], [8, 8], [11, 11]], [[3, 3], [6, 6], [9, 9], [12, 12]]]


def test_combine_channels():
    assert combine_channels([[[1]], [[2]]]) == [[[1, 2]]]
    assert combine_channels([[[1]], [[2]], [[3]]]) == [[[1, 2, 3]]]
    assert combine_channels([[[1, 3]], [[2, 4]]]) == [[[1, 2], [3, 4]]]
    assert combine_channels([[[1]], [[2]]]) == [[[1, 2]]]
    assert combine_channels([[[1, 1]], [[2, 2]]]) == [[[1, 2], [1, 2]]]
    assert combine_channels([[[1], [1]], [[2], [2]]]) == [[[1, 2]], [[1, 2]]]
    assert combine_channels(
        [[[1, 4], [7, 10]], [[2, 5], [8, 11]], [[3, 6], [9, 12]]]) == [
               [[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    assert combine_channels([[[1, 1], [4, 4],
                              [7, 7], [10, 10]],
                             [[2, 2], [5, 5],
                              [8, 8],
                              [11, 11]],
                             [[3, 3], [6, 6],
                              [9, 9], [12, 12]]]) == [[[1, 2, 3], [1, 2, 3]],
        [[4, 5, 6], [4, 5, 6]], [[7, 8, 9], [7, 8, 9]], [[10, 11, 12], [10, 11, 12]]]


def test_RGB2grayscale():
    assert RGB2grayscale([[[100, 180, 240]]]) == [[163]]
    assert RGB2grayscale([[[100, 180, 240], [100, 180, 240]],
                          [[100, 180, 240], [100, 180, 240]]]) == [[163, 163],
                                                                   [163, 163]]
    assert RGB2grayscale(
        [[[100, 180, 240], [1, 1, 1]], [[0, 0, 0], [-1, -2, 5]]]) == [[163, 1],
                                                                      [0, -1]]


def test_blur_kernel():
    assert blur_kernel(3) == [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9],
                              [1 / 9, 1 / 9, 1 / 9]]
    assert blur_kernel(11) == [[1 / 121] * 11] * 11
    assert blur_kernel(1) == [[1.0]]


def test_apply_kernel():
    assert apply_kernel([[0, 128, 255]], blur_kernel(3)) == [[14, 128, 241]]
    assert apply_kernel([[0, 128, 255]], blur_kernel(3)) == [[14, 128, 241]]
    assert apply_kernel([[1, 1, 5],
                         [7, 1, 0],
                         [3, 3, 3]], blur_kernel(3)) == [[2, 2, 4],
                                                         [4, 3, 1],
                                                         [3, 3, 2]]
    assert apply_kernel([[-5]], blur_kernel(1)) == [[0]]
    assert apply_kernel([[256]], blur_kernel(1)) == [[255]]


def test_bilinear_interpolation():
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 1) == 64
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112


def test_resize():
    assert resize([[0, 1], [2, 3]], 10, 10)[9][9] == 3
    assert resize([[0, 1], [2, 3]], 10, 10)[0][0] == 0
    assert resize([[0, 1], [2, 3]], 10, 10)[0][9] == 1
    assert resize([[0, 1], [2, 3]], 10, 10)[9][0] == 2


def test_rotate_90():
    assert rotate_90([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'R') == [[7, 4, 1],
                                                                 [8, 5, 2],
                                                                 [9, 6, 3]]

    assert rotate_90([[1, 2, 3], [4, 5, 6]], 'R') == [[4, 1],
                                                      [5, 2],
                                                      [6, 3]]
    assert rotate_90([[1, 2, 3], [4, 5, 6]], 'L') == [[3, 6],
                                                      [2, 5],
                                                      [1, 4]]
    assert rotate_90(
        [[[1, 2, 3], [2, 3, 4], [3, 4, 5]], [[4, 5, 6], [5, 6, 7], [6, 7, 8]]],
        'L') == [
               [[3, 4, 5], [6, 7, 8]],
               [[2, 3, 4], [5, 6, 7]],
               [[1, 2, 3], [4, 5, 6]]]

def test_get_edges():
    assert get_edges([[200, 50, 200]], 3, 3, 10) == [[255, 0, 255]]
    assert get_edges([[200, 50, 200], [200, 50, 200], [200, 50, 200]], 1, 3,
                     10) == [[255, 0, 255], [255, 0, 255], [255, 0, 255]]


def test_mask():
    assert add_mask([[50, 50, 50]], [[200, 200, 200]], [[0, 0.5, 1]]) == [
        [200, 125, 50]]