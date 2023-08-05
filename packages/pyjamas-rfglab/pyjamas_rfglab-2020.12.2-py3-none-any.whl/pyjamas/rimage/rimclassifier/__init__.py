"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from . import rimclassifier, rimlr, rimsvm, rimnn, featurecalculator, featurecalculator_sog, \
    featurecalculator_rowofpixels, featurecalculator_rawimage

__all__ = [rimclassifier.rimclassifier, rimlr.lr, rimsvm.svm, rimnn.DeepCNN, featurecalculator.FeatureCalculator,
           featurecalculator_sog.FeatureCalculatorSOG, featurecalculator_rowofpixels.FeatureCalculatorROP,
           featurecalculator_rawimage.FeatureCalculatorRawImage]
