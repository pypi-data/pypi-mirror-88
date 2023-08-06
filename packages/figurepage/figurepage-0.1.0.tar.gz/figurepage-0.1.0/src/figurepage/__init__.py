import argparse
import glob
import os
import string
import textwrap
import urllib.request
import webbrowser

# yapf: disable
html_source = string.Template(textwrap.dedent("""\
    <html>
    <title>$title</title>
    <script type="text/javascript">
      function changeFigureSize(numColumns, marginLR, marginTB) {
        var numFigures, startImageWidth, startImageHeight, aspectRatio;
        numFigures = document.images.length;
        for (var n = 1; n <= numFigures; n++) {
          imgElement = "figure" + (n + '');
          startImageWidth = document.images[imgElement].width;
          startImageHeight = document.images[imgElement].height;
          aspectRatio = startImageWidth / startImageHeight;
          imageWidth = (pageWidth() - marginLR) / numColumns;
          if (imageWidth / aspectRatio > pageHeight() - marginTB) {
            document.images[imgElement].width = (pageHeight() - marginTB) * aspectRatio;
            document.images[imgElement].height = (pageHeight() - marginTB);
          } else {
            document.images[imgElement].width = imageWidth;
            document.images[imgElement].height = imageWidth / aspectRatio;
          }
        }
      }
      function pageWidth() {
        if (window.innerWidth != null) {
          return window.innerWidth;
        } else if (document.documentElement && document.documentElement.clientWidth) {
          return document.documentElement.clientWidth;
        } else if (document.body != null) {
          return document.body.clientWidth;
        } else {
          return null;
        }
      }
      function pageHeight() {
        if (window.innerHeight != null) {
          return window.innerHeight;
        } else if (document.documentElement && document.documentElement.clientHeight) {
          return document.documentElement.clientHeight;
        } else if (document.body != null) {
          return document.body.clientHeight;
        } else {
          return null;
        }
      }
    </script>
    <style type="text/css">
      body {
        margin: 0;
      }
    
      div#header {
        position: fixed;
        width: 100%;
        padding-top: 0;
        margin-top: 0px;
        top: 0;
        left: 0;
        height: 40px;
        background-color: #B0B0B0;
      }
    
      @media screen {
        body>div#header {
          position: fixed;
        }
      }
    
      * html body {
        overflow: hidden;
      }
    
      * html div#content {
        height: 100%;
        overflow: auto;
      }
    
      div#header-title {
        float: left;
        padding-left: 25;
        font-size: 28px;
      }
    
      div#header-options {
        float: right;
        padding-right: 10;
        font-size: 14px;
      }
    
      div#content {
        padding: 40px 0 0 0;
      }
    
      p {
        margin-top: 3;
        font-family: Arial, Helvetica, sans-serif;
      }
    </style>
    </head>
    
    <body>
      <div id="header">
        <div id="header-title">
          <p>$title</p>
        </div>
        <div id="header-options">
          <p align="center">Number of Columns<br>
            <a onclick="changeFigureSize(1,50,50)" href="javascript:void(0);">1</a>
            <a onclick="changeFigureSize(2,55,50)" href="javascript:void(0);">2</a>
            <a onclick="changeFigureSize(3,60,50)" href="javascript:void(0);">3</a>
            <a onclick="changeFigureSize(4,65,50)" href="javascript:void(0);">4</a>
            <a onclick="changeFigureSize(5,70,50)" href="javascript:void(0);">5</a>
          </p>
        </div>
      </div>
      <div id="content">
        <p>
    $figures
        </p>
      </div>
    </body>
    
    </html>
"""))
# yapf: enable

figure_source = string.Template(
    '      <img name="$name" src="$source" width="$width" />')


def figurepage(title,
               sourcedir,
               output='figures.html',
               extensions=['png'],
               figwidth=300,
               openhtml=True):
    """
    Parameters
    ----------
    title : str
        Title of the page.
    sourcedir : path-like
        Directory where the images are.
    output : str, optional
        Name of the HTML file. (default: 'figures.html')
    extensions : list, optional
        File extensions to look for. (default: ['png'])
    """
    htmlfilepath = os.path.realpath(output)

    figfiles = []
    for ext in extensions:
        figfiles.extend(glob.glob(os.path.join(sourcedir, '*' + ext)))

    figcmds = '\n'.join([
        figure_source.substitute(
            name=f'figure{i}',
            source=os.path.relpath(file, start=os.path.dirname(htmlfilepath)),
            width=figwidth,
        ) for i, file in enumerate(figfiles)
    ])

    with open(htmlfilepath, 'w') as f:
        print(html_source.substitute(title=title, figures=figcmds), file=f)

    if openhtml:
        webbrowser.open('file://' + urllib.request.pathname2url(htmlfilepath))


def main():
    parser = argparse.ArgumentParser(
        description='Create an HTML file for displaying figures.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dir', help='Directory where image sources are.')
    parser.add_argument('--title',
                        '-t',
                        default='Figures',
                        help='Title of the page.')
    parser.add_argument('--output',
                        '-o',
                        default='figures.html',
                        help='Path for the output HTML file.'
                        ' Images will be referenced by their'
                        ' location relative to the output file.')
    parser.add_argument('--extensions',
                        '-e',
                        metavar='EXT',
                        default=['png'],
                        nargs='+',
                        help='File extensions to look for.')
    parser.add_argument('--width',
                        '-w',
                        default=300,
                        help='Initial figure width.')
    parser.add_argument('--open',
                        action='store_true',
                        help='Open the default web browser'
                        ' after creating the file.')

    args = parser.parse_args()
    figurepage(args.title, args.dir, args.output, args.extensions, args.width,
               args.open)
