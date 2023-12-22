`timescale 10ns/1ns

module tb_TRV32I;
    parameter B_WIDTH = 32;

    logic clk, rst;
    logic [31:0] pc, inst;
    logic bus_read_en, bus_write_en;
    logic [B_WIDTH-1:0] bus_read_data, bus_write_data;

    //connect topmodule
    TRV32I TRV32I(.clk(clk), .rst(rst), .inst(inst),
                    .bus_read_data(bus_read_data), .bus_read_en(bus_read_en),
                    .bus_write_data(bus_write_data), .bus_write_en(bus_write_en));
    
    //test bench start
    initial begin
            clk = 1'b1;
            rst = 1'b1;
        #3  rst = 1'b0;
    end

    always  #1  clk <= ~clk;


    always begin
        #2  $display($time, " clk= %b , rst= %b ,  pc= %h ,  inst= %h", clk, rst, pc, inst);

        TB_FINISH : assert (inst == 32'h00000073) begin
            #2  $display($time, " clk= %b , rst= %b ,  pc= %h ,  inst= %h", clk, rst, pc, inst);
            #6  $display($time, " FINISH");
            $finish;
        end

        TB_ERROR_ILLEGAL : assert (inst === 32'hxxxxxxxx) begin
            #2  $display($time, " clk= %b , rst= %b ,  pc= %h ,  inst= %h", clk, rst, pc, inst);
            #6  $display($time, " ERROR: inst ILLEGAL");
            $finish;
        end
    end


endmodule
