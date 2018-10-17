# This script will download all Phenocam images for a given month or set of months
# Created by Morgen Burke, October 2018
# The Imports Used
from bs4 import BeautifulSoup
import requests
import ntpath
from PIL import Image
import urllib, urllib2
import os

# List of possible days for the months in a year (probably a better way of doing this but it works)
day28 = list(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21',
              '22','23','24','25','26','27','28'])
day29 = list(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21',
              '22','23','24','25','26','27','28','29'])
day30 = list(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21',
              '22','23','24','25','26','27','28','29','30'])
day31 = list(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21',
              '22','23','24','25','26','27','28','29','30','31'])


def listFD(url):  # This gets the url for every image on a page
    page = requests.get(url).text
    # print page
    soup = BeautifulSoup(page, 'html.parser')
    image_list = list()
    # print soup
    for node in soup.find_all('a'):
        if str(node) is not None:
            if '.jpg' in str(node):
                # print('******')
                # print(str(node))
                image = str(node).split('\n', 1)[0]
                head, tail = ntpath.split(image)
                # print (tail[:-2])
                image_list.append(tail[:-2])
    return image_list


def download_images(the_images_list, output_location):  # This downloads and image and the associated meta file
    for an_image in the_images_list:
        image_path = image_archive + an_image
        current_image = Image.open(urllib2.urlopen(image_path))
        current_image.save(output_location+an_image)
        meta_path = image_path[:-3] + 'meta'
        metafile = urllib.URLopener()
        try:
            metafile.retrieve(meta_path, output_location + an_image[:-3] + 'meta')
        except:
            print("no meta file for: "+an_image)


def is_a_leap_year(f_year):  # Determines if a year is a leap year, to figure out how many days in February
    f_year = int(f_year)
    if f_year % 4 == 0:
        if f_year % 100 == 0:
            if f_year % 400 == 0:
                is_leap_year = True
            else:
                is_leap_year = False
        else:
            is_leap_year = True
    else:
        is_leap_year = False
    return is_leap_year


if __name__ == '__main__':

    # Information to change #################################
    site = 'usgseros'  # The site you want to get imagery for
    year = '2018'  # The year to download
    directory_for_data = 'output_images/'  # The output folder, needs to have a trailing /

    month = ['10']  # The month, or set of months within the year set above that imagery will be downloaded for

    # month = ['01','02','03','04','05','06','07','08','09','10','11','12']  # Use instead if you want all months
    ##########################################################

    # Start of recursive section
    if os.path.isdir(directory_for_data+year) is False:  # Makes a directory for the year if needed
        os.makedirs(directory_for_data+year)
    leap_year = is_a_leap_year(year)

    for the_month in month:  # Iterates through each month
        if the_month in list(['01','03','05','07','08','10','12']):
            choosen_day = day31
        elif the_month in list(['04','06','09','11']):
            choosen_day = day30
        else:
            if leap_year is True:
                choosen_day = day29
            else:
                choosen_day = day28

        os.makedirs(directory_for_data + year + '/' + str(the_month))  # Makes a directory for the month

        for the_day in choosen_day:  # Iterates through each day, below if the URL's for the phenocam site
            color_url = 'https://phenocam.sr.unh.edu/webcam/browse/'+site+'/'+year+'/'+str(the_month)+'/'+str(the_day)
            ir_url = 'https://phenocam.sr.unh.edu/webcam/browse/'+site+'_IR/'+year+'/'+str(the_month)+'/'+str(the_day)
            image_archive = 'https://phenocam.sr.unh.edu/data/archive/'+site+'/'+year+'/'+str(the_month)+'/'

            the_color_images = listFD(color_url)  # Gets a list of the color images
            the_ir_images = listFD(ir_url)  # Gets a list of the IR images
            # print(the_color_images)
            # print(the_ir_images)
            print(str(the_month)+":"+str(the_day))  # Prints to let you know what month:day it is downloading

            if len(the_color_images) > 0 and len(the_ir_images) > 0:  # Just a test to make sure there are images
                if the_color_images[0] is not '' and the_ir_images[0] is not '':  # Test to make sure list is not blank
                    # Downloads the color images
                    download_images(the_color_images, directory_for_data+year+'/'+str(the_month)+'/')
                    # Downloads the IR images
                    download_images(the_ir_images, directory_for_data+year+'/'+str(the_month)+'/')


