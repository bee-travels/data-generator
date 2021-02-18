/* janus-schema.groovy
 *
 * Sample usage in a gremlin.sh session:
 *
 * gremlin> :load data/janusgraph-schema-grateful-dead.groovy
 * ==>true
 * ==>true
 * gremlin> defineSchema(graph)
 * ==>null
 * gremlin>
 */

def defineSchema(graph) {
    mgmt = graph.openManagement()

    if (! mgmt.containsPropertyKey("object_type")) mgmt.makePropertyKey("object_type").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("id")) mgmt.makePropertyKey("id").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("name")) mgmt.makePropertyKey("name").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("is_hub")) mgmt.makePropertyKey("is_hub").dataType(Boolean.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("is_destination")) mgmt.makePropertyKey("is_destination").dataType(Boolean.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("type")) mgmt.makePropertyKey("type").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("city")) mgmt.makePropertyKey("city").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("country")) mgmt.makePropertyKey("country").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("latitude")) mgmt.makePropertyKey("latitude").dataType(Float.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("longitude")) mgmt.makePropertyKey("longitude").dataType(Float.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("gps_code")) mgmt.makePropertyKey("gps_code").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("iata_code")) mgmt.makePropertyKey("iata_code").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("source_airport_id")) mgmt.makePropertyKey("source_airport_id").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("destination_airport_id")) mgmt.makePropertyKey("destination_airport_id").dataType(String.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("flight_time")) mgmt.makePropertyKey("flight_time").dataType(Integer.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("flight_duration")) mgmt.makePropertyKey("flight_duration").dataType(Float.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("cost")) mgmt.makePropertyKey("cost").dataType(Float.class).cardinality(Cardinality.single).make()
    if (! mgmt.containsPropertyKey("airlines")) mgmt.makePropertyKey("airlines").dataType(String.class).cardinality(Cardinality.single).make()

    if(!mgmt.containsVertexLabel("airport")) mgmt.makeVertexLabel("airport").make()
    if(!mgmt.containsVertexLabel("flight")) mgmt.makeVertexLabel("flight").make()

    if(!mgmt.containsEdgeLabel("departing")) mgmt.makeEdgeLabel("departing").multiplicity(MULTI).make()
    if(!mgmt.containsEdgeLabel("arriving")) mgmt.makeEdgeLabel("arriving").multiplicity(MULTI).make()

    id_ = mgmt.getPropertyKey("id")
    city = mgmt.getPropertyKey("city")
    country = mgmt.getPropertyKey("country")
    iata_code = mgmt.getPropertyKey("iata_code")
    object_type = mgmt.getPropertyKey("object_type")

    airport = mgmt.getVertexLabel("airport")
    flight = mgmt.getVertexLabel("flight")

    mgmt.buildIndex("vertex_by_object_type", Vertex.class).addKey(object_type).buildCompositeIndex()
    mgmt.buildIndex("airport_by_id", Vertex.class).addKey(id_).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_city_country_code", Vertex.class).addKey(city).addKey(country).addKey(iata_code).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_city_country", Vertex.class).addKey(city).addKey(country).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_city_code", Vertex.class).addKey(city).addKey(iata_code).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_country_code", Vertex.class).addKey(country).addKey(iata_code).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_city", Vertex.class).addKey(city).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_country", Vertex.class).addKey(country).indexOnly(airport).buildCompositeIndex()
    mgmt.buildIndex("airport_by_code", Vertex.class).addKey(iata_code).indexOnly(airport).buildCompositeIndex()

    mgmt.commit()
}
