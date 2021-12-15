#include "envoy/config/trace/v3/http_tracer.pb.h"
#include "envoy/config/trace/v3/zipkin.pb.h"
#include "envoy/config/trace/v3/zipkin.pb.validate.h"
#include "envoy/registry/registry.h"

#include "source/extensions/tracers/zipkin/config.h"

#include "test/mocks/server/tracer_factory.h"
#include "test/mocks/server/tracer_factory_context.h"

#include "gmock/gmock.h"
#include "gtest/gtest.h"

using ::testing::Eq;

namespace Envoy {
namespace Extensions {
namespace Tracers {
namespace Zipkin {
namespace {

TEST(ZipkinTracerConfigTest, ZipkinHttpTracer) {
  NiceMock<Server::Configuration::MockTracerFactoryContext> context;
  context.server_factory_context_.cluster_manager_.initializeClusters({"fake_cluster"}, {});

  const std::string yaml_string = R"EOF(
  http:
    name: zipkin
    typed_config:
      "@type": type.googleapis.com/envoy.config.trace.v3.ZipkinConfig
      collector_cluster: fake_cluster
      collector_endpoint: /api/v2/spans
      collector_endpoint_version: HTTP_JSON
  )EOF";

  envoy::config::trace::v3::Tracing configuration;
  TestUtility::loadFromYaml(yaml_string, configuration);

  ZipkinTracerFactory factory;
  auto message = Config::Utility::translateToFactoryConfig(
      configuration.http(), ProtobufMessage::getStrictValidationVisitor(), factory);
  auto zipkin_tracer = factory.createTracerDriver(*message, context);
  EXPECT_NE(nullptr, zipkin_tracer);
}

TEST(ZipkinTracerConfigTest, ZipkinHttpTracerWithTypedConfig) {
  NiceMock<Server::Configuration::MockTracerFactoryContext> context;
  context.server_factory_context_.cluster_manager_.initializeClusters({"fake_cluster"}, {});

  const std::string yaml_string = R"EOF(
  http:
    name: zipkin
    typed_config:
      "@type": type.googleapis.com/envoy.config.trace.v3.ZipkinConfig
      collector_cluster: fake_cluster
      collector_endpoint: /api/v2/spans
      collector_endpoint_version: HTTP_PROTO
  )EOF";

  envoy::config::trace::v3::Tracing configuration;
  TestUtility::loadFromYaml(yaml_string, configuration);

  ZipkinTracerFactory factory;
  auto message = Config::Utility::translateToFactoryConfig(
      configuration.http(), ProtobufMessage::getStrictValidationVisitor(), factory);
  auto zipkin_tracer = factory.createTracerDriver(*message, context);
  EXPECT_NE(nullptr, zipkin_tracer);
}

// Test that the deprecated extension name is disabled by default.
// TODO(zuercher): remove when envoy.deprecated_features.allow_deprecated_extension_names is removed
TEST(ZipkinTracerConfigTest, DEPRECATED_FEATURE_TEST(DeprecatedExtensionFilterName)) {
  const std::string deprecated_name = "envoy.zipkin";

  ASSERT_EQ(nullptr, Registry::FactoryRegistry<Server::Configuration::TracerFactory>::getFactory(
                         deprecated_name));
}

} // namespace
} // namespace Zipkin
} // namespace Tracers
} // namespace Extensions
} // namespace Envoy
