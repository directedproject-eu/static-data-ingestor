<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld
                                                                                                 http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
  <NamedLayer>
    <Name>water_level_transparent</Name>
    <UserStyle>
      <FeatureTypeStyle>
        <Title>water_level_transparent</Title>
        <Rule>
          <RasterSymbolizer>
            <ColorMap extended = 'true' type='ramp'>
              <ColorMapEntry color = '#ffffff' quantity = '0.0' label='0.0' opacity='0.0'/>
              <ColorMapEntry color = '#1a68ae' quantity = '0.5' label='0.5' opacity='0.7'/>
              <ColorMapEntry color = '#08306b' quantity = '1.0' label='1.0' opacity='0.7'/>
              <ColorMapEntry color = '#301934' quantity = '11.0' label='11.0' opacity='0.7'/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>