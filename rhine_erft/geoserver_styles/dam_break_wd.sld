<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>blue_ramp_2m_steps_0_to_21</Name>
    <UserStyle>
      <Title>Blue Ramp (2m Steps, 0 to 21m)</Title>
      <Abstract>A blue colormap transition with 2m intervals for elevation/depth values between 0 and 21m, with 0m fully transparent.</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap type="ramp">
              <!-- Value 0m: Fully Transparent -->
              <ColorMapEntry color="#FFFFFF" quantity="0" opacity="0.0" label="0 m (Transparent)"/>
              
              <!-- 2m Step Intervals (>0m to 21m) -->
              <ColorMapEntry color="#87CEEB" quantity="0.01" opacity="1.0" label="> 0 m"/>
              <ColorMapEntry color="#6BAED6" quantity="2.0" opacity="1.0" label="2 m"/>
              <ColorMapEntry color="#4292C6" quantity="4.0" opacity="1.0" label="4 m"/>
              <ColorMapEntry color="#2171B5" quantity="6.0" opacity="1.0" label="6 m"/>
              <ColorMapEntry color="#1F69B2" quantity="8.0" opacity="1.0" label="8 m"/>
              <ColorMapEntry color="#1A5AA1" quantity="10.0" opacity="1.0" label="10 m"/>
              <ColorMapEntry color="#144C90" quantity="12.0" opacity="1.0" label="12 m"/>
              <ColorMapEntry color="#0E3E7E" quantity="14.0" opacity="1.0" label="14 m"/>
              <ColorMapEntry color="#0B306B" quantity="16.0" opacity="1.0" label="16 m"/>
              <ColorMapEntry color="#062258" quantity="18.0" opacity="1.0" label="18 m"/>
              <ColorMapEntry color="#031545" quantity="20.0" opacity="1.0" label="20 m"/>
              <ColorMapEntry color="#010A30" quantity="21.0" opacity="1.0" label="21 m"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

