<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld
                                                                                                 http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
  <NamedLayer>
    <Name>mean_flood_damage</Name>
    <UserStyle>
      <FeatureTypeStyle>
        <Title>mean_flood_damage</Title>
        <Rule>
          <RasterSymbolizer>
            <ColorMap type="intervals">
              <ColorMapEntry color = '#ffffff' quantity = '100000' label='Less than 100k DK' opacity='0.0'/>
              <ColorMapEntry color = '#F8D5D4' quantity = '500000' label='500k DK' opacity='0.7'/>
              <ColorMapEntry color = '#F2ABA8' quantity = '1000000' label='1M DK' opacity='0.7'/>
              <ColorMapEntry color = '#EB817D' quantity = '10000000' label='10M DK' opacity='0.7'/>
              <ColorMapEntry color = '#E55751' quantity = '20000000' label='20M DK' opacity='0.7'/>
              <ColorMapEntry color = '#DE2D26' quantity = '200000000' label='200M DK' opacity='0.7'/>
              <ColorMapEntry color = '#B2241E' quantity = '300000000' label='Greater than 200M DK' opacity='0.7'/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
