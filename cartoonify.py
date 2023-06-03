#################################################################
# FILE : cartoonify.py
# WRITER : Geva Haviv
# DESCRIPTION:
# WEB PAGES I USED:
# NOTES:
#################################################################

import math, copy, sys, ex5_helper

#This function separate the colors and returns the rows of same color image.
def single_color_row(row, i):
    return [cell[i] for cell in row]

#This function separate channels of image and returns number of images as number of colors.
def separate_channels(image):
    lst_of_images = []
    one_color_image =[]
    length_of_channels = len(image[0][0])

    for i in range(length_of_channels):
        for row in image:
            one_color_image.append(single_color_row(row, i))
        lst_of_images.append(one_color_image.copy())
        one_color_image.clear()

    return lst_of_images

#This function returns the combined color pixel for each pixel
def combine_pixel_color(channels, i, j):
    return [image[i][j] for image in channels]

#This function combine the different images from different colors and combine them to one image.
def combine_channels(channels):
    image = []
    row = []

    for row_number in range(len(channels[0])):
        for col_number in range(len(channels[0][0])):
            row.append(combine_pixel_color(channels, row_number, col_number))
        image.append(row.copy())
        row.clear()

    return image

#This function convert one colored pixel to grayscale.
def graysclae_pixel(pixel):
    graysclae_pixel = (pixel[0] * 0.299) + (pixel[1] * 0.587) + (pixel[2] * 0.114)
    return round(graysclae_pixel)

#This function convert the image to grayscale.
def RGB2grayscale(colored_image):
    grayscale_image = []
    grayscale_row = []

    for row_number in range(len(colored_image)):
        for col_number in range(len(colored_image[0])):
            colored_pixel = colored_image[row_number][col_number]
            grayscale_row.append(graysclae_pixel(colored_pixel))
        grayscale_image.append(grayscale_row.copy())
        grayscale_row.clear()

    return grayscale_image

#This function return blur kernel.
def blur_kernel(size):
    row = []
    kernel = []

    for row_number in range(size):
        for col_number in range(size):
            row.append(1 / (size * size))
        kernel.append(row.copy())
        row.clear()

    return kernel

#This function blur single pixel.
def blur_pixel(extended_image, kernel, pixel_value, row_to_start, col_to_start):
    sum = 0

    for row_index in range(len(kernel)):
        for col_index in range(len(kernel)):
            if extended_image[row_index + row_to_start][col_index + col_to_start] != 'None':
                sum += (extended_image[row_index + row_to_start][col_index + col_to_start] * kernel[row_index][col_index])
            else:
                sum += (pixel_value * kernel[row_index][col_index])

    if sum > 255:
        return 255
    elif sum < 0:
        return 0
    return round(sum)

#This function create new extended image for take care the edge's.
def create_extended_image(image, kernel):
    extended_image = []
    extended_row = []
    extended_by = len(kernel) // 2
    row_in_original_image = 0
    col_in_original_image = 0

    for row_index in range(len(image) + (2 * extended_by)):
        for col_index in range(len(image[0]) + (2 * extended_by)):
            if row_index <= extended_by - 1:
                extended_row.append('None')
            elif col_index <= extended_by - 1:
                extended_row.append('None')
            elif row_index >= len(image) + extended_by:
                extended_row.append('None')
            elif col_index >= len(image[0]) + extended_by:
                extended_row.append('None')
            else:
                extended_row.append(image[row_in_original_image][col_in_original_image])
                col_in_original_image += 1

        extended_image.append(extended_row.copy())
        extended_row.clear()
        col_in_original_image = 0
        if len(image) - 1 > row_in_original_image:
            row_in_original_image += 1

    return extended_image

#This function apply the kernel and return blured image.
def apply_kernel(image, kernel):
    blur_row = []
    blur_image = []
    extended_image = create_extended_image(image, kernel)

    for row_number in range(len(extended_image)):
        for col_number in range(len(extended_image[row_number])):
            if extended_image[row_number][col_number] != 'None':
                pixel_value = extended_image[row_number][col_number]
                row_to_start = row_number - (len(kernel) // 2)
                col_to_start = col_number - (len(kernel) // 2)
                blur_row.append(blur_pixel(extended_image, kernel, pixel_value , row_to_start, col_to_start))

        if len(blur_row) > 0:
            blur_image.append(blur_row.copy())
            blur_row.clear()

    return blur_image

#This function return the value of the new pixel.
def bilinear_interpolation(image, y, x):
    a = image[0][0]
    b = image[1][0]
    c = image[0][1]
    d = image[1][1]
    x1 = x - math.floor(x)
    y1 = y - math.floor(y)
    new_pixel = (a * (1 - x1) * (1 - y1)) + (b * y1 * (1 - x1)) + (c * x1 * (1 - y1)) + (d * x1 * y1)
    return round(new_pixel)

#This function create single image for interpolation.
def create_image_for_interpolation(image, row_index, col_index):
    image_for_interpolation = []
    row_for_interpolation = []

    for i in range(2):
        for j in range(2):
            row_for_interpolation.append(image[row_index][col_index])
        image_for_interpolation.append(row_for_interpolation.copy())
        row_for_interpolation.clear()

    return image_for_interpolation

#This function resize the image according to the parameters.
def resize(image, new_height, new_width):
    new_image = []
    new_row = []
    new_height = new_height / len(image[0])
    new_width = new_width / len(image)

    for row_index in range(int(len(image) * new_width)):
        for col_index in range(int(len(image[0]) * new_height)):
            if row_index % new_width == 0 and col_index % new_height == 0:
                new_row.append(image[int(row_index / new_width)][int(col_index / new_height)])
            else:
                image_for_interpolation = create_image_for_interpolation(image, int(row_index // new_width), int(col_index // new_height))
                new_row.append(bilinear_interpolation(image_for_interpolation, row_index / new_width, col_index / new_height))
                image_for_interpolation.clear()
        new_image.append(new_row.copy())
        new_row.clear()

    return new_image

#This function rotate the 2D image.
def rotate(img , direction):
    hight = len(img[0])
    width = len((img))
    rotate_img = []
    rotate_row = []

    if direction == 'R':
        for i in range(hight):
            for j in range(width, 0, -1):
                rotate_row.append(img[j - 1][i])
            rotate_img.append(rotate_row.copy())
            rotate_row.clear()

    elif direction == 'L':
        for i in range(hight, 0, -1):
            for j in range(width):
                rotate_row.append(img[j][i - 1])
            rotate_img.append(rotate_row.copy())
            rotate_row.clear()

    return rotate_img

#This function rotate the image by 90 degrees.
def rotate_90(image, direction):
    if type(image[0][0]) is list:
        img = separate_channels(image)
        for i in range(len(image[0][0])):
            img[i] = rotate(img[i], direction)
        img = combine_channels(img)
    else:
        img = rotate(image, direction)

    return img

#This function calculate the avg.
def avg(block, i, j, r, pixel_value):
    sum = 0
    count = 0

    for row in range(i - r, i + r + 1):
        for col in range(j - r, j + r + 1):
            if block[row][col] == 'None':
                sum += pixel_value
                count += 1
            else:
                sum += block[row][col]
                count += 1

    return sum / count

#This function get the edges of the image.
def get_edges(image, blur_size, block_size, c):
    blured_image = apply_kernel(image, blur_kernel(blur_size))
    block = create_extended_image(blured_image, blur_kernel(block_size))
    r = block_size // 2
    new_row = []
    new_image = []

    for i in range(len(image)):
        for j in range(len(image[i])):
            threshold = avg(block, i, j, r, blured_image[i][j])
            if blured_image[i][j] < threshold - c:
                new_row.append(0)
            else:
                new_row.append(255)
        new_image.append(new_row.copy())
        new_row.clear()

    return new_image

#This function is the formula for quantize.
def formula_for_quantize(pixel_value, N):
    return round(math.floor(pixel_value * (N / 255)) * (255 / N))

#This function quantize the colors.
def quantize(image, N):
    qrow = []
    qimage = []

    for i in range(len(image)):
        for j in range(len(image[i])):
            qrow.append(formula_for_quantize(image[i][j], N))
        qimage.append(qrow.copy())
        qrow.clear()

    return qimage

#This function quantize the colors of 3D image.
def quantize_color_image(image, N):
    channels = separate_channels(image)
    for i in range(len(channels)):
        channels[i] = quantize(channels[i], N)

    return combine_channels(channels)

#This function is the formula for mask.
def formula_for_mask(pixel_1, pixel_2, pixel_mask):
    return round(pixel_1 * pixel_mask + pixel_2 * (1 - pixel_mask))

#This function mix between images for each channel.
def add_mask_for_single_channel(channel_1, channel_2, mask):
    new_row = []
    new_image = []

    for i in range(len(channel_1)):
        for j in range(len(channel_1[i])):
            new_row.append(formula_for_mask(channel_1[i][j], channel_2[i][j], mask[i][j]))
        new_image.append(new_row.copy())
        new_row.clear()

    return new_image

#This function create mask.
def create_mask(grayscale_img):
    mask = copy.deepcopy(grayscale_img)

    for i in range(len(grayscale_img)):
        for j in range(len(grayscale_img[i])):
            mask[i][j] = grayscale_img[i][j] / 255

    return mask

#This function mix between images.
def add_mask(image1, image2, mask):
    img = []

    if type(image1[0][0]) is list:
        length = len(image1[0][0])
        img1 = separate_channels(image1)
        img2 = separate_channels(image2)
        for i in range(length):
            img.append(add_mask_for_single_channel(img1[i], img2[i], mask))
        img = combine_channels(img)
    else:
        img = add_mask_for_single_channel(image1, image2, mask)

    return img

def cartoonify(image, blur_size, th_block_size, th_c, quant_num_shades):
    grayscale_img = RGB2grayscale(image)
    edge_img = get_edges(grayscale_img, blur_size, th_block_size, th_c)
    mask = create_mask(edge_img)
    channels = quantize_color_image(image, quant_num_shades)
    channels = separate_channels(channels)

    for i in range(len(channels)):
        channels[i] = add_mask(channels[i], edge_img, mask)

    cartoonify_image = combine_channels(channels)
    return cartoonify_image

def resize_3D_image(img, w, h):
    new_img = separate_channels(img)

    for i in range(len(new_img)):
        new_img[i] = resize(new_img[i], w, h)

    return combine_channels(new_img)

if __name__ == '__main__':
    if len(sys.argv) != 8:
        sys.exit('Error.')
    else:
        image_source = sys.argv[1]
        cartoon_dest = sys.argv[2]
        max_im_size = int(sys.argv[3])
        blur_size = int(sys.argv[4])
        th_block_size = int(sys.argv[5])
        th_c = int(sys.argv[6])
        quant_num_shades = int(sys.argv[7])
        img = ex5_helper.load_image(image_source)

        if len(img[0]) > max_im_size:
            new_img = resize_3D_image(img, max_im_size, int(max_im_size * (len(img) / len(img[0]))))
        elif len(img) > max_im_size:
            new_img = resize_3D_image(img, int(max_im_size * (len(img[0]) / len(img))), max_im_size)

        new_img = cartoonify(new_img, blur_size, th_block_size, th_c, quant_num_shades)
        ex5_helper.save_image(new_img, cartoon_dest)


